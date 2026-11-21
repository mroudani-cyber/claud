"""
Voice AI assistant: PC microphone -> Groq Whisper (speech-to-text) -> Groq LLM
-> speaks the answer through the PC speaker and shows it on the Arduino LCD.

Setup:
    pip install groq pyserial sounddevice numpy scipy pyttsx3 unidecode
    set GROQ_API_KEY=your_key_here          (Windows cmd)
    python assistant.py --port COM5         (use your Arduino's COM port)

Press Enter to start talking, press Enter again to stop.
Type 'q' then Enter to quit.
"""
import argparse
import os
import tempfile
import time

import numpy as np
import pyttsx3
import serial
import sounddevice as sd
from groq import Groq
from scipy.io import wavfile
from unidecode import unidecode

SAMPLE_RATE = 16000
CHAT_MODEL = "llama-3.3-70b-versatile"
STT_MODEL = "whisper-large-v3-turbo"
SYSTEM_PROMPT = (
    "You are a helpful voice assistant shown on a tiny 16x2 screen. "
    "Answer in 1-2 short sentences, plain text, no emojis or markdown."
)


class Display:
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)  # Arduino resets when the port opens

    def send(self, line):
        # LCD only supports plain ASCII: convert accents, Arabic, etc.
        text = unidecode(line).replace("\n", " ")[:290]
        self.ser.write((text + "\n").encode("ascii", "ignore"))

    def status(self, text):
        self.send("S:" + text)

    def answer(self, text):
        self.send("A:" + text)

    def idle(self):
        self.send("I")


def record_until_enter():
    chunks = []

    def callback(indata, frames, t, status):
        chunks.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback):
        input("  Recording... press Enter to stop.")
    if not chunks:
        return None
    audio = np.concatenate(chunks)
    path = os.path.join(tempfile.gettempdir(), "ai_question.wav")
    wavfile.write(path, SAMPLE_RATE, audio)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Arduino port, e.g. COM5")
    args = parser.parse_args()

    client = Groq()  # reads GROQ_API_KEY from the environment
    display = Display(args.port)
    tts = pyttsx3.init()
    tts.setProperty("rate", 175)
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    display.idle()
    print("Ready! Press Enter to talk, or type q + Enter to quit.")

    while True:
        if input("> ").strip().lower() == "q":
            break

        display.status("LISTENING")
        wav = record_until_enter()
        if not wav:
            display.idle()
            continue

        display.status("THINKING")
        with open(wav, "rb") as f:
            question = client.audio.transcriptions.create(
                file=("q.wav", f.read()), model=STT_MODEL
            ).text.strip()
        print("You:", question)
        if not question:
            display.idle()
            continue

        history.append({"role": "user", "content": question})
        reply = client.chat.completions.create(
            model=CHAT_MODEL, messages=history[-11:], max_tokens=120
        ).choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        print("AI:", reply)

        display.answer(reply)
        tts.say(reply)
        tts.runAndWait()

    display.idle()


if __name__ == "__main__":
    main()
