import os

def get_groq_api_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise EnvironmentError("❌ GROQ_API_KEY not set. Please run: export GROQ_API_KEY=...")
    return key

def get_hf_api_key():
    key = os.getenv("HUGGINGFACE_API_KEY")
    if not key:
        raise EnvironmentError("❌ HUGGINGFACE_API_KEY not set. Please run: export HUGGINGFACE_API_KEY=...")
    return key