import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
model_name = 'llama-3.3-70b-versatile'

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')