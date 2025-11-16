import tkinter as tk
from tkinter import ttk, messagebox
import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import pyttsx3
from gtts import gTTS
from playsound import playsound   # For playback, playsound is simplest cross-platform (use playsound 1.2.2)

# --- Load API key ---
load_dotenv()
api_key = os.getenv("api")
genai.configure(api_key=api_key)
print("API Key loaded:", bool(api_key))

# --- Supported languages ---
LANGUAGES = ["Hindi","English", "Marathi", "French", "Spanish", "German", "Tamil", "Gujarati", "Japanese"]
# add this mapping after LANGUAGES
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

# --- Text-to-speech setup ---
tts_engine = pyttsx3.init()

# --- Translation using Gemini ---
def translate_text(text, target_language):
    try:
        prompt = (
            f"Translate the following text into {target_language}. "
            f"Give only the translated text, no explanation, no quotes:\n\n{text}"
        )
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        return translated_text
    except Exception as e:
        return f"Error: {e}"

# --- Voice recognition using sounddevice ---
def recognize_speech():
    recognizer = sr.Recognizer()
    fs = 16000  # sample rate
    duration = 5  # seconds of recording
    messagebox.showinfo("Voice Input", "🎤 Speak now...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    audio = sr.AudioData(audio_data.tobytes(), fs, 2)

    try:
        text = recognizer.recognize_google(audio)
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, text)
        messagebox.showinfo("Voice Input", f"Captured text:\n{text}")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I couldn't understand your voice.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not request results; check your internet connection.")

# --- Speak translated text aloud ---
def speak_text():
    """
    Speak the translated text. Uses gTTS (Google TTS) keyed to the selected
    target language. If gTTS or audio playback fails, falls back to pyttsx3.
    """
    text = output_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No translated text to speak.")
        return

    # Determine language code from selected language (default to English)
    target = language_var.get()
    lang_code = LANG_CODE.get(target, "en")

    # Try gTTS -> save temp mp3 -> play -> remove
    try:
        # create a temporary file
        fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # close file descriptor, gTTS will write by path

        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(tmp_path)

        # play the file (blocking)
        playsound(tmp_path)

        # cleanup
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    except Exception as gerr:
        # fallback to pyttsx3 if gTTS or playsound fails
        try:
            # optional: attempt to set voice matching language if available
            # many systems don't have matching voice names — this is a best-effort
            for voice in tts_engine.getProperty("voices"):
                vname = getattr(voice, "name", "") or getattr(voice, "id", "")
                if lang_code in vname.lower() or target.lower() in vname.lower():
                    tts_engine.setProperty("voice", voice.id)
                    break

            tts_engine.say(text)
            tts_engine.runAndWait()

        except Exception as perr:
            messagebox.showerror(
                "TTS Error",
                f"Could not play audio.\nPrimary error: {gerr}\nFallback error: {perr}"
            )


# --- Handle translation ---
def handle_translate():
    input_text = input_box.get("1.0", tk.END).strip()
    target_language = language_var.get()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter or speak text to translate.")
        return
    if target_language == "Select Language":
        messagebox.showwarning("Warning", "Please select a target language.")
        return

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Translating...")
    translated = translate_text(input_text, target_language)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, translated)

# --- GUI setup ---
root = tk.Tk()
root.title("Voice-Enabled Language Translator (Gemini-2.5)")
root.geometry("750x520")
root.resizable(False, False)

tk.Label(root, text="🎧 Voice-Enabled Translator powered by Gemini-2.5", font=("Times New Roman", 16, "bold")).pack(pady=10)
tk.Label(root, text="Enter or Speak Text:", font=("Arial", 11)).pack()
# Speak Button
tk.Button(root, text="🎤 Voice Input", command=recognize_speech, bg="#4CAF50", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

input_box = tk.Text(root, height=5, wrap="word", font=("Times New Roman", 11))
input_box.pack(fill="x", padx=15, pady=5)

language_var = tk.StringVar(value="Select Language")
language_menu = ttk.Combobox(root, textvariable=language_var, values=LANGUAGES, state="readonly", font=("Times New Roman", 11))
language_menu.pack(pady=10)

# Translate Button
tk.Button(root, text="🌐 Translate", command=handle_translate, bg="#2196F3", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

tk.Label(root, text="Translation:", font=("Times New Roman", 11)).pack()
output_box = tk.Text(root, height=5, wrap="word", font=("Times New Roman", 11), bg="#f7f7f7")
output_box.pack(fill="x", padx=15, pady=5)
# Output Reading Button
tk.Button(root, text="🔊 Speak Output", command=speak_text, bg="#9C27B0", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

root.mainloop()