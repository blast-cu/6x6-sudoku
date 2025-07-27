import os
import multiprocessing
from src import prompts
from src.config import get_groq_api_key, get_hf_api_key

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None


def read_file(path):
  with open(path, 'r') as file:
    lines = file.readlines()
  return lines


def write_file(path, data):
  with open(path, 'w') as file:
    file.write(data)


def strip_ascii(lines):
  formatted_output = []
  for line in lines:
    if '+' in line or '-' in line:
        continue
    clean_line = [elem.strip() if elem.strip() else '0' for elem in line.split('|')]
    formatted_output.append(' '.join(clean_line[1:-1]))

  formatted_output_result = '\n'.join(formatted_output)
  return formatted_output_result


def run_inference_groq(prompt, model_name, result):
    try:
        if Groq is None:
            raise ImportError("Groq SDK not installed. Run: pip install groq")

        client = Groq(api_key=get_groq_api_key())
        messages = [{"role": "user", "content": prompt}]
        response_text = ""

        output = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
            stream=True,
            max_tokens=8192,
            top_p=0.5
        )
        for chunk in output:
            response_text += chunk.choices[0].delta.content or ""

        result.put(response_text.strip())

    except Exception as e:
        print("Groq Inference Error:", e)
        result.put(None)


def run_inference_hf(prompt, model_name, result):
    try:
        if InferenceClient is None:
            raise ImportError("huggingface_hub not installed. Run: pip install huggingface_hub")

        client = InferenceClient( provider="auto", token=get_hf_api_key())
        messages = [{"role": "user", "content": prompt}]
        response_text = ""

        output = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
            stream=True,
            top_p=0.5
        )
        for chunk in output:
            response_text += chunk.choices[0].delta.content or ""

        result.put(response_text.strip())

    except Exception as e:
        print("HF Inference Error:", e)
        result.put(None)


def inference_with_timeout(sudoku_input, model_name, use_groq=True, timeout=120):
    prompt = prompts.Task_with_zero_shot.format(sudoku_input)
    result = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=run_inference_groq if use_groq else run_inference_hf,
        args=(prompt, model_name, result)
    )

    process.start()
    process.join(timeout)

    if process.is_alive():
        print("Inference timed out. Terminating.")
        process.terminate()
        process.join()
        return None

    return result.get()


def solve_sudoku_puzzles(
    input_dir="data/6x6Puzzles",
    output_base_dir="results",
    model_name="gemma2-9b-it",
    use_groq=True
):
    output_dir = os.path.join(output_base_dir, model_name.replace("/", "_"))
    os.makedirs(output_dir, exist_ok=True)
    solved_ids = set(os.listdir(output_dir))

    for idx, hashid in enumerate(os.listdir(input_dir)[:1]):
        if hashid in solved_ids:
            print(f"Skipping {hashid} since already solved by {model_name}")
            continue

        print(f"Processing {hashid} ({idx+1})")
        input_path = os.path.join(input_dir, hashid, "input.txt")
        lines = read_file(input_path)
        formatted_input = strip_ascii(lines)
        print("Formatted input:\n", formatted_input)

        model_output = inference_with_timeout(formatted_input, model_name, use_groq)

        if model_output is None:
            print(f"Inference failed or timed out for {hashid}")
            continue

        model_output = model_output.strip("Here is the completed 6x6 grid:").strip()
        print("Model output:\n", model_output)

        output_folder = os.path.join(output_dir, hashid)
        os.makedirs(output_folder, exist_ok=True)
        write_file(os.path.join(output_folder, "solved.txt"), model_output)
        solved_ids.add(hashid)
