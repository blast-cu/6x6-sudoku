# 6x6-sudoku

# The SE Solver
"Sukaku6Explainer.jar" is from the [official repository](https://github.com/1to9only/Sukaku6x6Explainer/releases), and its usage instructions are provided in the [main README](https://github.com/1to9only/Sukaku6x6Explainer)

### Running on macOS
Mac users can run the SE Solver using the following commands in Terminal:
```bash
cd /path/to/Sukaku6Explainer.jar
java -jar Sukaku6Explainer.jar
```
Make sure Java is installed and accessible via the `java` command.

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/blast-cu/6x6-sudoku.git
cd 6x6-sudoku
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🔐 API Key Setup

You need to set the appropriate API key as an environment variable depending on the model.

| Model Name                                | Caller       | Required Environment Variable |
|-------------------------------------------|--------------|-------------------------------|
| `gemma2-9b-it`                            | Groq         | `GROQ_API_KEY`                |
| `mistralai/Mistral-7B-Instruct-v0.3`      | Hugging Face | `HUGGINGFACE_API_KEY`         |
| `meta-llama/Llama-3.1-70B-Instruct`       | Hugging Face | `HUGGINGFACE_API_KEY`         |
| `meta-llama/Llama-3.1-8B-Instruct`        | Hugging Face | `HUGGINGFACE_API_KEY`         |

### Set your key before running:

#### Groq:
```bash
export GROQ_API_KEY=your_groq_api_key
```

#### Hugging Face:
```bash
export HUGGINGFACE_API_KEY=your_huggingface_api_key
```

---

## 🚀 Running Inference

To run inference, edit `run_inference.py` and set:

- `model_name` to the desired model
- `use_groq = True` for Groq models  
- `use_groq = False` for Hugging Face models

Then run:

```bash
python run_inference.py
```

Outputs will be saved in:

```
results/<model_name>/<puzzle_id>/solved.txt
```

## 📁 Folder Structure

```
.
├── data/
│   └── 6x6Puzzles/                 # Input puzzles
├── results/
│   └── <model_name>/<puzzle_id>/  # Inference results
├── src/
│   ├── utils.py                   # Inference and file I/O
│   ├── config.py                  # API key access
│   └── prompts.py                 # Prompt templates
├── run_inference.py               # Entrypoint (edit this to switch models)
├── requirements.txt
└── README.md
```
