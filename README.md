# 🎧 Voice-Enabled Modular Language Translator (Gemini 2.5)

A fully modular Python project that provides:
- Voice input (speech → text)
- Translation using Gemini 2.5 Flash
- Text-to-speech output
- Clean modular architecture for scalability
- Tkinter-based GUI

---

## 🚀 Features
- Translate any language supported by Gemini
- Speak input using microphone
- Speak translated text aloud
- Fully modular code inside the `modules/` folder

---

## 📁 Project Structure
voice-translator-modular/
│── main.py
│── requirements.txt
│── README.md
│
├── modules/
│     ├── api_config.py
│     ├── translator.py
│     ├── voice_input.py
│     ├── text_to_speech.py
│     └── gui.py

---

## 🛠 Install Dependencies
pip install -r requirements.txt

## ▶️ Run the App
python main.py

---

## 📌 Tech Used
- Python 3.11+
- Gemini 2.5 Flash API
- Tkinter GUI
- SpeechRecognition + SoundDevice
- gTTS + pyttsx3

---

## 📄 License
Free to use & modify.

