import tempfile
import os
import pyttsx3
from gtts import gTTS
from playsound import playsound
from tkinter import messagebox

tts_engine = pyttsx3.init()

LANG_CODE = {
    "Hindi": "hi",
    "English": "en",
    "Marathi": "mr",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Japanese": "ja",
}

def speak(text, target_language):
    if not text:
        messagebox.showwarning("Warning", "No translated text to speak.")
        return

    lang_code = LANG_CODE.get(target_language, "en")

    try:
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(path)

        playsound(path)
        os.remove(path)

    except Exception:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except:
            messagebox.showerror("Error", "Unable to play audio.")
