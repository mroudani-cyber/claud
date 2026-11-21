"""
Interactive voice AI assistant.

  Clap (sound sensor on the Arduino) or press Enter  ->  start listening
  Speak into the PC microphone; it stops automatically when you go quiet
  Groq Whisper turns speech into text, a Groq LLM answers
  The answer is spoken through the PC speaker and scrolls on the LCD
  The AI knows the live temperature/humidity from the DHT11

Setup:
    pip install groq pyserial sounddevice numpy scipy pyttsx3 unidecode
    set GROQ_API_KEY=your_key_here
    python assistant.py              (finds the Arduino automatically)
    python assistant.py --port COM5  (or choose the port yourself)

Say "goodbye" or press Ctrl+C to quit.
"""
import argparse
import io
import queue
import sys
import threading
import time

import numpy as np
import pyttsx3
import serial
import serial.tools.list_ports
import sounddevice as sd
from groq import Groq
from scipy.io import wavfile
from unidecode import unidecode

SAMPLE_RATE = 16000
CHAT_MODEL = "llama-3.3-70b-versatile"
STT_MODEL = "whisper-large-v3-turbo"
SILENCE_LEVEL = 500      # raise if it never stops recording (noisy room)
SILENCE_SECONDS = 1.2
MAX_SECONDS = 12

events = queue.Queue()
sensor = {"temp": None, "hum": None}


def find_port():
    for p in serial.tools.list_ports.comports():
        desc = f"{p.description} {p.manufacturer}".lower()
        if any(k in desc for k in ("arduino", "ch340", "ch341", "usb-serial", "usb serial")):
            return p.device
    ports = [p.device for p in serial.tools.list_ports.comports()]
    sys.exit(f"Arduino not found. Ports seen: {ports}. Use --port COMx")


class Display:
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=0.1)
        self.lock = threading.Lock()
        time.sleep(2.5)  # Arduino restarts when the port opens
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while True:
            try:
                line = self.ser.readline().decode("ascii", "ignore").strip()
            except serial.SerialException:
                events.put("disconnected")
                return
            if line == "C":
                events.put("clap")
            elif line.startswith("T:"):
                try:
                    t, h = line[2:].split(",")
                    sensor["temp"], sensor["hum"] = float(t), float(h)
                except ValueError:
                    pass

    def send(self, text):
        text = unidecode(text).replace("\n", " ")[:195]
        with self.lock:
            self.ser.write((text + "\n").encode("ascii", "ignore"))

    def status(self, t): self.send("S:" + t)
    def answer(self, t): self.send("A:" + t)
    def idle(self): self.send("I")


def keyboard_listener():
    while True:
        try:
            input()
        except EOFError:
            return
        events.put("enter")


def record():
    """Record until the user stops talking. Returns WAV bytes or None."""
    frames, spoke, quiet_since = [], False, None
    start = time.time()
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
        while time.time() - start < MAX_SECONDS:
            block, _ = stream.read(1600)  # 0.1 s
            frames.append(block)
            loud = np.abs(block).mean() > SILENCE_LEVEL
            if loud:
                spoke, quiet_since = True, None
            elif spoke:
                quiet_since = quiet_since or time.time()
                if time.time() - quiet_since > SILENCE_SECONDS:
                    break
            elif time.time() - start > 5:
                return None  # nobody talked
    buf = io.BytesIO()
    wavfile.write(buf, SAMPLE_RATE, np.concatenate(frames))
    return buf.getvalue()


def system_prompt():
    room = ""
    if sensor["temp"] is not None:
        room = (f" The room sensor currently reads {sensor['temp']:.1f} C "
                f"and {sensor['hum']:.0f}% humidity; use it if asked about the room.")
    return ("You are a friendly voice assistant living in a small Arduino gadget "
            "with a 16x2 screen. Reply in the user's language, in 1-2 short "
            "sentences, plain text, no emojis or markdown." + room)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", help="Arduino port, e.g. COM5")
    args = ap.parse_args()

    try:
        client = Groq()
    except Exception:
        sys.exit("No API key. Run:  set GROQ_API_KEY=your_key_here")

    port = args.port or find_port()
    print("Connecting to Arduino on", port)
    try:
        display = Display(port)
    except serial.SerialException as e:
        sys.exit(f"Can't open {port}: {e}\nClose the Arduino Serial Monitor and try again.")

    tts = pyttsx3.init()
    tts.setProperty("rate", 175)
    history = []
    threading.Thread(target=keyboard_listener, daemon=True).start()

    display.idle()
    print("Ready! Clap or press Enter to talk. Ctrl+C to quit.")

    while True:
        ev = events.get()
        if ev == "disconnected":
            sys.exit("Arduino disconnected.")
        while not events.empty():          # ignore extra claps
            events.get_nowait()

        display.status("LISTENING")
        print("Listening...")
        try:
            wav = record()
        except Exception as e:
            print("Microphone error:", e)
            display.answer("Microphone error")
            continue
        if not wav:
            display.idle()
            print("Didn't hear anything.")
            continue

        display.status("THINKING")
        try:
            question = client.audio.transcriptions.create(
                file=("q.wav", wav), model=STT_MODEL).text.strip()
            print("You:", question)
            if not question:
                display.idle()
                continue
            history.append({"role": "user", "content": question})
            reply = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[{"role": "system", "content": system_prompt()}] + history[-10:],
                max_tokens=120,
            ).choices[0].message.content.strip()
            history.append({"role": "assistant", "content": reply})
        except Exception as e:
            print("AI error:", e)
            display.answer("AI error - check internet / API key")
            continue

        print("AI:", reply)
        display.answer(reply)
        tts.say(reply)
        tts.runAndWait()

        if any(w in question.lower() for w in ("goodbye", "bye bye", "au revoir")):
            break

    display.idle()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
