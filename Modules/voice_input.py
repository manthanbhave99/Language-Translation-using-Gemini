import speech_recognition as sr
import sounddevice as sd
import numpy as np
from tkinter import messagebox

def recognize_speech(input_box):
    recognizer = sr.Recognizer()
    fs = 16000
    duration = 5

    messagebox.showinfo("Voice Input", "🎤 Speak now...")

    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    audio = sr.AudioData(audio_data.tobytes(), fs, 2)

    try:
        text = recognizer.recognize_google(audio)
        input_box.delete("1.0", "end")
        input_box.insert("end", text)
        messagebox.showinfo("Voice Input", f"Captured text:\n{text}")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I couldn't understand your voice.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not request results; check your internet.")
