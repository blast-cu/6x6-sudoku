from src import utils

"""
Choose your model and set the correct API key:

- If using 'gemma2-9b-it' → export GROQ_API_KEY = "{key}" before running
- If using "mistralai/Mistral-7B-Instruct-v0.3", 
           "meta-llama/Llama-3.1-70B-Instruct" 
           "meta-llama/Llama-3.1-8B-Instruct"
           → export HUGGINGFACE_API_KEY = "{key}" before running
"""

if __name__ == "__main__":
    utils.solve_sudoku_puzzles(
        model_name="mistralai/Mistral-7B-Instruct-v0.3", # change
        use_groq=False #False if using hugging face
    )