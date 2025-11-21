import google.generativeai as genai

def translate_text(text, target_language):
    try:
        prompt = (
            f"Translate the following text into {target_language}. "
            f"Give only the translated text, no explanation, no quotes:\n\n{text}"
        )
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
