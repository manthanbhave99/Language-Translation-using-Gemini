import tkinter as tk
from tkinter import ttk, messagebox

from modules.translator import translate_text
from modules.voice_input import recognize_speech
from modules.text_to_speech import speak

LANGUAGES = ["Hindi", "English", "Marathi", "French", "Spanish", "German", "Tamil", "Gujarati", "Japanese"]

def launch_gui():
    root = tk.Tk()
    root.title("Voice-Enabled Language Translator")
    root.geometry("750x520")
    root.resizable(False, False)

    tk.Label(root, text="🎧 Voice-Enabled Translator (Gemini 2.5)", font=("Times New Roman", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Enter or Speak Text:", font=("Arial", 11)).pack()

    input_box = tk.Text(root, height=5, wrap="word", font=("Times New Roman", 11))
    input_box.pack(fill="x", padx=15, pady=5)

    tk.Button(root, text="🎤 Voice Input", command=lambda: recognize_speech(input_box),
              bg="#4CAF50", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

    language_var = tk.StringVar(value="English")
    language_menu = ttk.Combobox(root, textvariable=language_var, values=LANGUAGES,
                                 state="readonly", font=("Times New Roman", 11))
    language_menu.pack(pady=10)

    output_box = tk.Text(root, height=5, wrap="word", font=("Times New Roman", 11), bg="#f7f7f7")
    output_box.pack(fill="x", padx=15, pady=5)

    def handle_translation():
        text = input_box.get("1.0", "end").strip()
        lang = language_var.get()

        if not text:
            messagebox.showwarning("Warning", "Enter text to translate.")
            return

        output_box.delete("1.0", "end")
        output_box.insert("end", "Translating...")

        translated = translate_text(text, lang)
        output_box.delete("1.0", "end")
        output_box.insert("end", translated)

    tk.Button(root, text="🌐 Translate", command=handle_translation,
              bg="#2196F3", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

    tk.Button(root, text="🔊 Speak Output",
              command=lambda: speak(output_box.get("1.0", "end").strip(), language_var.get()),
              bg="#9C27B0", fg="white", font=("Times New Roman", 12, "bold")).pack(pady=5)

    root.mainloop()
