import os
from dotenv import load_dotenv
import google.generativeai as genai

def load_api():
    load_dotenv()
    api_key = os.getenv("api")
    genai.configure(api_key=api_key)
    return api_key
