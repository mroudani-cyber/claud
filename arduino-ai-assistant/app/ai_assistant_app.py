"""
AI Assistant - Windows desktop app for the Arduino LCD voice assistant.

Talk with the mic button, Ctrl+Space, a clap on the KY-037, or type.
Answers are spoken, shown in the chat and scrolled on the 16x2 LCD.
Live DHT11 readings are shown in the sidebar and given to the AI.
The app updates itself from GitHub when started through launcher.py / the exe.
"""
import io
import json
import math
import random
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import re
import urllib.error
import urllib.request
import wave
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import numpy as np
import serial
import serial.tools.list_ports
import sounddevice as sd
from groq import Groq
from unidecode import unidecode

APP_NAME = "AI Assistant"
APP_VERSION = "2.2.0"

SAMPLE_RATE = 16000
STT_MODEL = "whisper-large-v3-turbo"
CHAT_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
PROVIDERS = ["Groq (online)", "Ollama (local)"]
STT_ENGINES = ["Groq Whisper (online)", "Windows (offline)"]
DEFAULT_OLLAMA_URL = "http://localhost:11434"
BUZZER_MODES = ["Off", "Beeps", "Beeps + robot voice"]
MIC_SENS = {"Low": (3.0, 250), "Medium": (2.0, 80), "High": (1.5, 35)}   # (x background noise, minimum)
WIN_CULTURES = {"en": "en-US", "fr": "fr-FR", "ar": "ar-SA", "es": "es-ES", "de": "de-DE"}
MAX_SECONDS = 15
IS_WIN = sys.platform == "win32"
NO_WINDOW = 0x08000000 if IS_WIN else 0

DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "AIAssistant")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
CHAT_FILE = os.path.join(DATA_DIR, "chat.json")
UPDATE_DIR = os.path.join(DATA_DIR, "app")
DEFAULT_UPDATE_URL = ("https://raw.githubusercontent.com/mroudani-cyber/claud/"
                      "ccr-b780153b-lpg5le/arduino-ai-assistant/app/")

LANGUAGES = {"Auto": None, "English": "en", "French": "fr", "Arabic": "ar",
             "Spanish": "es", "German": "de"}
PERSONALITIES = {
    "Friendly": "You are warm, cheerful and helpful.",
    "Funny": "You are playful and make light jokes, but still answer the question.",
    "Teacher": "You explain things simply and clearly, like a patient teacher.",
    "Robot": "You talk like a polite little robot, with a few beeps like 'beep boop'.",
    "Pirate": "You talk like a friendly pirate.",
    "Custom": "",
}
LENGTHS = {"Short": ("1-2 short sentences", 120),
           "Medium": ("3-5 sentences", 260),
           "Long": ("a detailed answer", 600)}
ACCENTS = {"Violet": "#7C5CFF", "Ocean": "#2F80ED", "Mint": "#12B886",
           "Sunset": "#FF7A45", "Rose": "#E84393", "Gold": "#E0A100"}
FONT_SIZES = {"Small": 12, "Medium": 14, "Large": 17}

DEFAULTS = {
    "api_key": "", "port": "", "auto_connect": True, "model": CHAT_MODELS[0],
    "provider": PROVIDERS[0], "ollama_url": DEFAULT_OLLAMA_URL, "ollama_model": "llama3.2",
    "stt": STT_ENGINES[0],
    "assistant_name": "Nova", "personality": "Friendly", "custom_prompt": "",
    "language": "Auto", "length": "Short",
    "speak": True, "voice": "", "voice_rate": 1, "voice_volume": 100,
    "silence_level": 500, "clap_enabled": True, "lcd_answers": True,
    "mic_device": "", "mic_sens": "Medium", "buzzer": BUZZER_MODES[2], "clap_sens": 20, "show_face": True,
    "theme": "Dark", "accent": "Violet", "font_size": "Medium",
    "unit": "C", "alert_enabled": False, "alert_temp": 30,
    "remember_chat": True, "auto_update": True, "update_url": DEFAULT_UPDATE_URL,
    "quick_prompts": ["How is the room?", "Tell me a joke", "What time is it?",
                      "Give me a fun fact"],
}

# light / dark colour pairs
BG = ("#F3F4F8", "#0F1117")
PANEL = ("#FFFFFF", "#171A23")
CARD = ("#E9EBF2", "#1F2330")
AI_BUBBLE = ("#E4E6EF", "#252A38")
TEXT = ("#151722", "#F2F3F7")
MUTED = ("#6B7185", "#8A90A6")
GREEN, RED, AMBER, BLUE = "#2DBE7E", "#FF5C7A", "#FFB547", "#4FC3F7"
FONT = "Segoe UI"


def shade(hex_color, factor=0.85):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * factor))) for c in (r, g, b))


def ver_tuple(v):
    try:
        return tuple(int(x) for x in str(v).split("."))
    except ValueError:
        return (0,)


# ---------------------------------------------------------------- storage
def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_config():
    cfg = dict(DEFAULTS)
    cfg.update(load_json(CONFIG_FILE, {}))
    if not cfg["api_key"]:
        cfg["api_key"] = os.environ.get("GROQ_API_KEY", "")
    return cfg


# ---------------------------------------------------------------- updates
def check_for_update(base_url):
    """Download a newer app version into UPDATE_DIR. Returns info dict or None."""
    base = base_url.rstrip("/") + "/"
    with urllib.request.urlopen(base + "version.json", timeout=10) as r:
        info = json.loads(r.read().decode("utf-8"))
    if ver_tuple(info.get("version")) <= ver_tuple(APP_VERSION):
        return None
    if os.environ.get("AIA_LAUNCHER") != "1":
        info["manual"] = True          # running the .py directly: just notify
        return info
    with urllib.request.urlopen(base + "ai_assistant_app.py", timeout=30) as r:
        code = r.read()
    compile(code, "ai_assistant_app.py", "exec")   # refuse broken downloads
    os.makedirs(UPDATE_DIR, exist_ok=True)
    target = os.path.join(UPDATE_DIR, "ai_assistant_app.py")
    with open(target + ".tmp", "wb") as f:
        f.write(code)
    os.replace(target + ".tmp", target)
    return info


def restart_app():
    if getattr(sys, "frozen", False):
        subprocess.Popen([sys.executable])
    else:
        subprocess.Popen([sys.executable, os.path.abspath(sys.argv[0])])


# ---------------------------------------------------------------- PowerShell helpers
def ps_command(ps):
    return ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command",
            "$ErrorActionPreference = 'Stop'; " + ps]


def run_ps(ps, timeout=60):
    return subprocess.run(ps_command(ps), stdin=subprocess.DEVNULL, capture_output=True,
                          timeout=timeout, creationflags=NO_WINDOW)


def ps_error(err_bytes):
    err = err_bytes.decode("utf-8", "ignore")
    found = re.findall(r'<S S="Error">(.*?)</S>', err)      # PowerShell's CLIXML error format
    text = " ".join(found) if found else err
    text = re.sub(r"_x000D__x000A_|\s+", " ", text).strip()
    return text[:220] or "unknown error"


def ps_quote(text):
    return text.replace("'", "''")


# ---------------------------------------------------------------- local AI (Ollama)
def ollama_request(base, path, payload=None, timeout=10):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(base.rstrip("/") + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def ollama_models(base):
    return sorted(m["name"] for m in ollama_request(base, "/api/tags").get("models", []))


def ollama_chat(base, model, messages, max_tokens):
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"num_predict": max_tokens * 3}}
    try:
        res = ollama_request(base, "/api/chat", payload, timeout=300)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise RuntimeError(f"OLLAMA_NO_MODEL:{model}")
        raise
    except urllib.error.URLError:
        raise RuntimeError("OLLAMA_OFFLINE")
    text = res.get("message", {}).get("content", "")
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()  # hide "thinking" models' notes


# ---------------------------------------------------------------- offline speech recognition
def windows_stt(wav, lang=None):
    """Speech-to-text with the recognizer built into Windows (no internet)."""
    if not IS_WIN:
        raise RuntimeError("WIN_STT:Offline speech recognition only works on Windows")
    fd, path = tempfile.mkstemp(suffix=".wav")
    with os.fdopen(fd, "wb") as f:
        f.write(wav)
    make = "New-Object System.Speech.Recognition.SpeechRecognitionEngine"
    culture = WIN_CULTURES.get(lang or "")
    engine = (f"try {{ $r = {make}([System.Globalization.CultureInfo]'{culture}') }} catch {{ $r = {make} }}; "
              if culture else f"$r = {make}; ")
    ps = ("[Console]::OutputEncoding = [Text.Encoding]::UTF8; Add-Type -AssemblyName System.Speech; "
          + engine + "$r.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar)); "
          f"$r.SetInputToWaveFile('{path}'); $out = @(); "
          "while ($res = $r.Recognize()) { $out += $res.Text }; $r.Dispose(); $out -join ' '")
    try:
        out = run_ps(ps, timeout=90)
        text = out.stdout.decode("utf-8", "ignore").strip()
        if out.returncode != 0 and not text:
            raise RuntimeError("WIN_STT:" + ps_error(out.stderr))
        return text
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


# ---------------------------------------------------------------- speech out
def clean_for_speech(text):
    text = re.sub(r"[*#_`>~|]", " ", text)                                # markdown symbols
    text = re.sub("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]", " ", text)   # emojis
    return re.sub(r"\s+", " ", text).strip()


def speech_lang(text, setting):
    code = LANGUAGES.get(setting)
    if code:
        return code
    if re.search("[\u0600-\u06FF]", text):
        return "ar"
    return ""


class Speaker:
    """Speaks with the Windows voices. Tries System.Speech first, then the classic SAPI engine."""

    def __init__(self):
        self.proc = None
        self.stopped = False
        self.last_error = ""

    def speak(self, text, voice="", rate=1, volume=100, lang=""):
        """Returns True when spoken (or stopped by the user), False on failure (see last_error)."""
        text = clean_for_speech(text)
        if not text:
            return True
        self.stopped = False
        if not IS_WIN:
            try:
                import pyttsx3
                e = pyttsx3.init()
                e.say(text)
                e.runAndWait()
                return True
            except Exception as ex:
                self.last_error = str(ex)
                return False

        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        rate = max(-10, min(10, int(rate)))
        volume = max(0, min(100, int(volume)))
        read = f"$t = Get-Content -Raw -Encoding UTF8 -LiteralPath '{ps_quote(path)}'; "
        if voice:
            select = f"try {{ $s.SelectVoice('{ps_quote(voice)}') }} catch {{}}; "
        elif lang:
            select = ("$v = $s.GetInstalledVoices() | Where-Object { $_.Enabled -and "
                      f"$_.VoiceInfo.Culture.Name -like '{lang}*' }} | Select-Object -First 1; "
                      "if ($v) { $s.SelectVoice($v.VoiceInfo.Name) }; ")
        else:
            select = ""
        engines = [
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SetOutputToDefaultAudioDevice(); "
            + select + f"$s.Rate = {rate}; $s.Volume = {volume}; " + read + "$s.Speak($t); $s.Dispose()",
            # backup engine: the classic SAPI voice (works on PCs where System.Speech is broken)
            f"$v = New-Object -ComObject SAPI.SpVoice; $v.Rate = {rate}; $v.Volume = {volume}; "
            + read + "[void]$v.Speak($t)",
        ]
        try:
            for ps in engines:
                self.proc = subprocess.Popen(ps_command(ps), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, creationflags=NO_WINDOW)
                _, err = self.proc.communicate()
                if self.stopped:
                    return True
                if self.proc.returncode == 0:
                    return True
                self.last_error = ps_error(err)
            return False
        except FileNotFoundError:
            self.last_error = "PowerShell was not found on this PC"
            return False
        except Exception as ex:
            self.last_error = str(ex)
            return False
        finally:
            self.proc = None
            try:
                os.remove(path)
            except OSError:
                pass

    def stop(self):
        self.stopped = True
        p = self.proc
        if p and p.poll() is None:
            p.kill()

    @staticmethod
    def list_voices():
        if not IS_WIN:
            return []
        ps = ("Add-Type -AssemblyName System.Speech; "
              "(New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() | "
              "Where-Object { $_.Enabled } | ForEach-Object { $_.VoiceInfo.Name + ' (' + $_.VoiceInfo.Culture.Name + ')' }")
        try:
            out = run_ps(ps, timeout=20).stdout.decode("utf-8", "ignore")
            return [v.strip() for v in out.splitlines() if v.strip()]
        except Exception:
            return []


# ---------------------------------------------------------------- microphone
def list_mics():
    """Input devices (one entry per microphone)."""
    out, seen = [], set()
    try:
        apis = sd.query_hostapis()
        for i, d in enumerate(sd.query_devices()):
            if d["max_input_channels"] < 1:
                continue
            if IS_WIN and "MME" not in apis[d["hostapi"]]["name"]:
                continue
            name = d["name"].strip()
            if name not in seen and "mapper" not in name.lower():
                seen.add(name)
                out.append(name)
    except Exception:
        pass
    return out


def mic_index(name):
    if not name:
        return None
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0 and d["name"].strip() == name:
            return i
    return None


def to_wav16k(audio, rate):
    """float32 mono -> 16 kHz 16-bit WAV bytes."""
    if rate != SAMPLE_RATE and len(audio) > 1:
        n = int(len(audio) * SAMPLE_RATE / rate)
        audio = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio)
    pcm = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    return buf.getvalue()


def record_speech(device_name, sens, on_level=None, should_stop=None, max_seconds=MAX_SECONDS, fixed=False):
    """Record until the speaker goes quiet. Learns the room noise first, so quiet mics work too.
    Returns (wav_bytes or None, info dict)."""
    dev = mic_index(device_name)
    rate = int(sd.query_devices(dev if dev is not None else sd.default.device[0])["default_samplerate"])
    block = int(rate * 0.05)
    factor, floor = MIC_SENS.get(sens, MIC_SENS["Medium"])
    frames, rms_hist = [], []
    spoke, quiet_since, peak = False, None, 0.0
    start = time.time()
    with sd.InputStream(device=dev, samplerate=rate, channels=1, dtype="float32", blocksize=block) as st:
        while time.time() - start < max_seconds:
            data, _ = st.read(block)
            data = data[:, 0].copy()
            frames.append(data)
            rms = float(np.sqrt(np.mean(data ** 2))) * 32767
            peak = max(peak, rms)
            rms_hist.append(rms)
            elapsed = time.time() - start
            if elapsed < 0.4:                       # learn the background noise (and skip the beep)
                if on_level:
                    on_level(0.0)
                continue
            noise = float(np.percentile(rms_hist[:8], 30))
            thr = min(max(noise * factor, floor), 1500)
            if on_level:
                on_level(min(1.0, rms / (thr * 2.5)))
            if should_stop and should_stop():
                break
            if fixed:
                continue
            if rms > thr:
                spoke, quiet_since = True, None
            elif spoke:
                quiet_since = quiet_since or time.time()
                if time.time() - quiet_since > 1.3:
                    break
            elif elapsed > 7:
                break
    noise = float(np.percentile(rms_hist[:8], 30)) if rms_hist else 0
    info = {"peak": peak, "noise": noise, "spoke": spoke}
    if peak < 15:
        info["problem"] = "silent"
        return None, info
    if not spoke and not fixed and not (should_stop and should_stop()) and peak < max(noise * 1.3, floor * 0.6):
        info["problem"] = "nothing"
        return None, info
    return to_wav16k(np.concatenate(frames), rate), info


# ---------------------------------------------------------------- arduino link
class Arduino:
    def __init__(self, port, events):
        self.events = events
        self.ser = serial.Serial(port, 115200, timeout=0.1)
        self.lock = threading.Lock()
        self.alive = True
        time.sleep(2.5)  # board restarts when the port opens
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while self.alive:
            try:
                line = self.ser.readline().decode("ascii", "ignore").strip()
            except Exception:
                if self.alive:
                    self.events.put(("disconnected", None))
                return
            if line == "C":
                self.events.put(("clap", None))
            elif line.startswith("T:"):
                try:
                    t, h = line[2:].split(",")
                    self.events.put(("sensor", (float(t), float(h))))
                except ValueError:
                    pass
            elif line.startswith("L:"):
                try:
                    lv, avg, do = line[2:].split(",")
                    self.events.put(("mic_sensor", (int(lv), int(avg), do.strip() == "1")))
                except ValueError:
                    pass

    def send(self, text):
        text = unidecode(text).replace("\n", " ")[:195]
        try:
            with self.lock:
                self.ser.write((text + "\n").encode("ascii", "ignore"))
        except (serial.SerialException, OSError):
            pass

    def close(self):
        try:
            self.send("I")
            self.alive = False
            self.ser.cancel_read()
            self.ser.close()
        except Exception:
            pass


def list_ports():
    return [(p.device, f"{p.device} - {p.description}") for p in serial.tools.list_ports.comports()]


ARDUINO_HINTS = ("arduino", "ch340", "ch341", "usb-serial", "usb serial", "ch9102", "cp210")


def guess_port(ports, strict=False):
    for dev, label in ports:
        if any(k in label.lower() for k in ARDUINO_HINTS):
            return dev
    return "" if strict or not ports else ports[0][0]


# ---------------------------------------------------------------- settings window
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.accent = app.accent
        self.title("Settings")
        self.geometry("580x640")
        self.minsize(480, 420)
        self.configure(fg_color=PANEL)
        self.transient(app)
        self.after(150, self._focus)
        cfg = app.cfg

        # Buttons are packed FIRST at the bottom so they are always visible.
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(side="bottom", fill="x", padx=20, pady=16)
        ctk.CTkButton(btns, text="Save", height=42, fg_color=self.accent, hover_color=shade(self.accent),
                      font=(FONT, 14, "bold"), command=self.save).pack(side="right", fill="x", expand=True)
        ctk.CTkButton(btns, text="Cancel", height=42, width=110, fg_color=CARD, text_color=TEXT,
                      hover_color=AI_BUBBLE, command=self.destroy).pack(side="left", padx=(0, 10))

        tabs = ctk.CTkTabview(self, fg_color=PANEL, segmented_button_selected_color=self.accent,
                              segmented_button_selected_hover_color=shade(self.accent))
        tabs.pack(fill="both", expand=True, padx=12, pady=(8, 0))
        pages = {}
        for name in ("General", "AI", "Voice", "Look", "Arduino", "Updates"):
            tabs.add(name)
            sf = ctk.CTkScrollableFrame(tabs.tab(name), fg_color="transparent")
            sf.pack(fill="both", expand=True)
            pages[name] = sf

        # ----- General
        p = pages["General"]
        self._label(p, "Groq API key", "Free at console.groq.com - not needed with Ollama + Windows speech")
        krow = ctk.CTkFrame(p, fg_color="transparent")
        krow.pack(fill="x", pady=4)
        self.key = ctk.CTkEntry(krow, show="•", height=36)
        self.key.insert(0, cfg["api_key"])
        self.key.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(krow, text="👁", width=40, height=36, fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                      command=lambda: self.key.configure(show="" if self.key.cget("show") else "•")
                      ).pack(side="left", padx=6)
        self.key.bind("<Return>", lambda e: self.save())
        self._label(p, "Assistant name")
        self.name = ctk.CTkEntry(p, height=36)
        self.name.insert(0, cfg["assistant_name"])
        self.name.pack(fill="x", pady=4)
        self.remember = self._switch(p, "Remember conversations between sessions", cfg["remember_chat"])
        self._label(p, "Quick buttons", "One per line - shown above the message box")
        self.quick = ctk.CTkTextbox(p, height=110)
        self.quick.insert("1.0", "\n".join(cfg["quick_prompts"]))
        self.quick.pack(fill="x", pady=4)

        # ----- AI
        p = pages["AI"]
        self._label(p, "AI brain", "Groq = online and fast · Ollama = runs on this PC, free and offline")
        self.provider = self._segment(p, PROVIDERS, cfg["provider"])
        self._label(p, "Groq model", "70b = smartest, 8b = fastest")
        self.model = self._menu(p, CHAT_MODELS, cfg["model"])
        self._label(p, "Ollama model", "Install models with:  ollama pull llama3.2")
        orow = ctk.CTkFrame(p, fg_color="transparent")
        orow.pack(fill="x", pady=4)
        self.ollama_model = ctk.CTkComboBox(orow, values=[cfg["ollama_model"]], height=34, fg_color=CARD,
                                            text_color=TEXT, button_color=self.accent,
                                            button_hover_color=shade(self.accent))
        self.ollama_model.set(cfg["ollama_model"])
        self.ollama_model.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(orow, text="⟳", width=40, height=34, fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                      command=self._load_ollama).pack(side="left", padx=6)
        self.ollama_status = ctk.CTkLabel(p, text="", text_color=MUTED, font=(FONT, 11))
        self.ollama_status.pack(anchor="w")
        self._label(p, "Ollama address")
        self.ollama_url = ctk.CTkEntry(p, height=34)
        self.ollama_url.insert(0, cfg["ollama_url"])
        self.ollama_url.pack(fill="x", pady=4)
        self.after(300, self._load_ollama)
        self._label(p, "Personality")
        self.personality = self._segment(p, list(PERSONALITIES), cfg["personality"])
        self._label(p, "Custom instructions", "Used with the Custom personality (or added to any other)")
        self.custom = ctk.CTkTextbox(p, height=90)
        self.custom.insert("1.0", cfg["custom_prompt"])
        self.custom.pack(fill="x", pady=4)
        self._label(p, "Language", "Language you speak and the AI answers in")
        self.language = self._menu(p, list(LANGUAGES), cfg["language"])
        self._label(p, "Answer length")
        self.length = self._segment(p, list(LENGTHS), cfg["length"])

        # ----- Voice
        p = pages["Voice"]
        self.speak = self._switch(p, "Speak answers out loud", cfg["speak"])
        self._label(p, "Voice", "Windows voices installed on this PC")
        self.voice = self._menu(p, [cfg["voice"] or "Default"], cfg["voice"] or "Default")
        threading.Thread(target=self._load_voices, daemon=True).start()
        self._label(p, "Speed")
        self.rate = self._slider(p, -5, 5, cfg["voice_rate"], 10)
        self._label(p, "Volume")
        self.volume = self._slider(p, 10, 100, cfg["voice_volume"], 9)
        ctk.CTkButton(p, text="▶  Test voice", fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                      command=self._test_voice).pack(anchor="w", pady=(8, 0))
        self.voice_status = ctk.CTkLabel(p, text="", text_color=MUTED, font=(FONT, 11), wraplength=480,
                                         justify="left")
        self.voice_status.pack(anchor="w", pady=(2, 6))
        self._label(p, "Speech recognition", "Windows (offline) needs no internet or key - works best in English")
        self.stt = self._segment(p, STT_ENGINES, cfg["stt"])
        self._label(p, "Microphone", "Pick the mic you talk into")
        mics = ["Default"] + list_mics()
        self.mic = self._menu(p, mics, cfg["mic_device"] if cfg["mic_device"] in mics else "Default")
        self._label(p, "Mic sensitivity", "High = catches quiet voices · Low = for noisy rooms")
        self.mic_sens = self._segment(p, list(MIC_SENS), cfg["mic_sens"])
        mrow = ctk.CTkFrame(p, fg_color="transparent")
        mrow.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(mrow, text="🎙  Test microphone (3 s)", fg_color=CARD, text_color=TEXT,
                      hover_color=AI_BUBBLE, command=self._test_mic).pack(side="left")
        self.mic_bar = ctk.CTkProgressBar(mrow, progress_color=self.accent)
        self.mic_bar.set(0)
        self.mic_bar.pack(side="left", fill="x", expand=True, padx=10)
        self.mic_status = ctk.CTkLabel(p, text="", text_color=MUTED, font=(FONT, 11), wraplength=480,
                                       justify="left")
        self.mic_status.pack(anchor="w", pady=(2, 6))

        # ----- Look
        p = pages["Look"]
        self._label(p, "Theme")
        self.theme = self._segment(p, ["Dark", "Light", "System"], cfg["theme"])
        self._label(p, "Accent colour")
        arow = ctk.CTkFrame(p, fg_color="transparent")
        arow.pack(fill="x", pady=4)
        self.accent_var = ctk.StringVar(value=cfg["accent"])
        for n, c in ACCENTS.items():
            ctk.CTkRadioButton(arow, text=n, variable=self.accent_var, value=n, fg_color=c,
                               hover_color=shade(c), width=80).pack(side="left", padx=2)
        self._label(p, "Text size")
        self.font_size = self._segment(p, list(FONT_SIZES), cfg["font_size"])
        self._label(p, "Temperature unit")
        self.unit = self._segment(p, ["C", "F"], cfg["unit"])
        self.show_face = self._switch(p, "Show the animated face", cfg["show_face"])

        # ----- Arduino
        p = pages["Arduino"]
        self.auto_connect = self._switch(p, "Connect automatically at startup", cfg["auto_connect"])
        self.clap = self._switch(p, "Clap to talk (KY-037 sound sensor)", cfg["clap_enabled"])
        self.lcd = self._switch(p, "Show answers on the LCD", cfg["lcd_answers"])
        self._label(p, "Buzzer (pin 13)", "Beeps when listening/answering · robot voice chirps while it talks")
        self.buzzer = self._segment(p, BUZZER_MODES, cfg["buzzer"])
        ctk.CTkButton(p, text="🔔  Test buzzer", fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                      command=self._test_buzzer).pack(anchor="w", pady=6)
        self._label(p, "Clap sensitivity", "Lower number = reacts to softer claps")
        self.clap_sens = self._slider(p, 3, 100, cfg["clap_sens"], 97)
        self.clap_sens.configure(command=lambda v: (self._slider_lbl(self.clap_sens, v), self._send_clap_sens(v)))
        self.monitor = ctk.CTkSwitch(p, text="Clap sensor test (shows the live sound level)", text_color=TEXT,
                                     progress_color=self.accent, command=self._toggle_monitor)
        self.monitor.pack(anchor="w", pady=6)
        self.sensor_bar = ctk.CTkProgressBar(p, progress_color=self.accent)
        self.sensor_bar.set(0)
        self.sensor_bar.pack(fill="x", pady=2)
        self.sensor_status = ctk.CTkLabel(p, text="", text_color=MUTED, font=(FONT, 11), wraplength=480,
                                          justify="left")
        self.sensor_status.pack(anchor="w")
        self.alert = self._switch(p, "Warn me when the room gets too hot", cfg["alert_enabled"])
        self._label(p, "Hot room warning at (°C)")
        self.alert_temp = self._slider(p, 20, 45, cfg["alert_temp"], 25)
        self._label(p, "Send your own text to the LCD")
        lrow = ctk.CTkFrame(p, fg_color="transparent")
        lrow.pack(fill="x", pady=4)
        self.lcd_text = ctk.CTkEntry(lrow, height=36, placeholder_text="Hello world!")
        self.lcd_text.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(lrow, text="Send", width=70, height=36, fg_color=self.accent, hover_color=shade(self.accent),
                      command=self._send_lcd).pack(side="left", padx=6)

        # ----- Updates
        p = pages["Updates"]
        self._label(p, f"Version {APP_VERSION}", "Updates are downloaded from GitHub")
        self.auto_update = self._switch(p, "Check for updates at startup", cfg["auto_update"])
        ctk.CTkButton(p, text="⟳  Check now", fg_color=self.accent, hover_color=shade(self.accent),
                      command=lambda: app.check_updates(manual=True)).pack(anchor="w", pady=8)
        self._label(p, "Update address (advanced)")
        self.update_url = ctk.CTkEntry(p, height=36)
        self.update_url.insert(0, cfg["update_url"])
        self.update_url.pack(fill="x", pady=4)

    # ---------- small builders
    def _focus(self):
        self.lift()
        self.focus_force()
        try:
            self.grab_set()
        except Exception:
            pass

    def _label(self, parent, text, hint=None):
        ctk.CTkLabel(parent, text=text, text_color=TEXT, font=(FONT, 13, "bold")).pack(anchor="w", pady=(12, 0))
        if hint:
            ctk.CTkLabel(parent, text=hint, text_color=MUTED, font=(FONT, 11)).pack(anchor="w")

    def _switch(self, parent, text, on):
        s = ctk.CTkSwitch(parent, text=text, text_color=TEXT, progress_color=self.accent)
        if on:
            s.select()
        s.pack(anchor="w", pady=6)
        return s

    def _menu(self, parent, values, current):
        m = ctk.CTkOptionMenu(parent, values=values, fg_color=CARD, text_color=TEXT,
                              button_color=self.accent, button_hover_color=shade(self.accent))
        m.set(current)
        m.pack(fill="x", pady=4)
        return m

    def _segment(self, parent, values, current):
        s = ctk.CTkSegmentedButton(parent, values=values, selected_color=self.accent,
                                   selected_hover_color=shade(self.accent))
        s.set(current)
        s.pack(fill="x", pady=4)
        return s

    def _slider(self, parent, lo, hi, value, steps=None):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)
        lbl = ctk.CTkLabel(row, text=str(int(value)), width=44, text_color=MUTED)
        lbl.pack(side="right")
        s = ctk.CTkSlider(row, from_=lo, to=hi, number_of_steps=steps, button_color=self.accent,
                          progress_color=self.accent, command=lambda v: lbl.configure(text=str(int(round(v)))))
        s.value_label = lbl
        s.set(value)
        s.pack(side="left", fill="x", expand=True)
        return s

    def _load_voices(self):
        voices = Speaker.list_voices()
        if voices:
            self.after(0, lambda: self.voice.configure(values=["Default"] + voices))

    def _load_ollama(self):
        url = self.ollama_url.get().strip() or DEFAULT_OLLAMA_URL
        self.ollama_status.configure(text="Looking for Ollama…", text_color=MUTED)

        def work():
            try:
                models = ollama_models(url)
                msg = (f"✓ Ollama is running · {len(models)} model(s) installed" if models
                       else "✓ Ollama is running, but no models yet: run  ollama pull llama3.2")
                ok = (models, msg, GREEN if models else AMBER)
            except Exception:
                ok = (None, f"✗ Ollama not found at {url} - install it from ollama.com and open it", RED)
            self.after(0, lambda: self._ollama_done(*ok))
        threading.Thread(target=work, daemon=True).start()

    def _ollama_done(self, models, msg, color):
        if not self.winfo_exists():
            return
        self.ollama_status.configure(text=msg, text_color=color)
        if models:
            self.ollama_model.configure(values=models)
            if self.ollama_model.get() not in models:
                self.ollama_model.set(models[0])

    @staticmethod
    def _slider_lbl(slider, v):
        slider.value_label.configure(text=str(int(round(v))))

    def _send_clap_sens(self, v):
        if self.app.arduino:
            self.app.arduino.send(f"K:{int(round(v))}")

    def _test_buzzer(self):
        if not self.app.arduino:
            self.sensor_status.configure(text="Connect the Arduino first.", text_color=AMBER)
            return
        self.app.arduino.send(f"B:{BUZZER_MODES.index(self.buzzer.get())}")
        self.app.arduino.send("P:test")
        if self.buzzer.get() == "Off":
            self.sensor_status.configure(text="The buzzer is set to Off.", text_color=AMBER)

    def _toggle_monitor(self):
        on = bool(self.monitor.get())
        if not self.app.arduino:
            self.monitor.deselect()
            self.sensor_status.configure(text="Connect the Arduino first.", text_color=AMBER)
            return
        self._send_clap_sens(self.clap_sens.get())
        self.app.arduino.send("M:1" if on else "M:0")
        self.sensor_status.configure(text="Clap near the sensor…" if on else "", text_color=MUTED)
        if not on:
            self.sensor_bar.set(0)

    def on_mic_sensor(self, level, avg, do):
        thr = avg * 2 + self.clap_sens.get()
        self.sensor_bar.set(min(1.0, level / max(1, thr * 1.5)))
        txt = f"Sound level {level}  ·  background {avg}  ·  a clap needs more than {int(thr)}"
        if do:
            txt += "  ·  DO pin triggered"
        self.sensor_status.configure(text=txt, text_color=MUTED)

    def on_clap(self):
        self.sensor_status.configure(text="👏 Clap detected!", text_color=GREEN)

    def _test_mic(self):
        dev = "" if self.mic.get() == "Default" else self.mic.get()
        sens = self.mic_sens.get()
        self.mic_status.configure(text="Recording… say something!", text_color=MUTED)

        def level(v):
            self.after(0, lambda: self.winfo_exists() and self.mic_bar.set(v))

        def work():
            try:
                wav, info = record_speech(dev, sens, level, max_seconds=3, fixed=True)
                if info.get("problem") == "silent":
                    msg, col = ("✗ The mic gives no sound. Pick another microphone above, and check Windows "
                                "Settings > Privacy > Microphone ('Let desktop apps access your microphone').", RED)
                elif info["peak"] < max(info["noise"] * 2, 60):
                    msg, col = (f"⚠ Very quiet (loudest {info['peak']:.0f}). Speak closer, choose High "
                                "sensitivity, or raise the mic volume in Windows sound settings.", AMBER)
                else:
                    msg, col = (f"✓ Mic works (loudest {info['peak']:.0f}, background {info['noise']:.0f}).", GREEN)
            except Exception as e:
                msg, col = f"✗ Microphone error: {e}", RED
            self.after(0, lambda: self.winfo_exists() and (self.mic_status.configure(text=msg, text_color=col),
                                                           self.mic_bar.set(0)))
        threading.Thread(target=work, daemon=True).start()

    def destroy(self):
        if self.app.arduino:
            self.app.arduino.send("M:0")
        super().destroy()

    def _voice_value(self):
        v = self.voice.get()
        return "" if v == "Default" else re.sub(r" \([a-zA-Z-]+\)$", "", v)

    def _test_voice(self):
        text = f"Hi, I'm {self.name.get().strip() or 'Nova'}. This is how I sound."
        args = (text, self._voice_value(), int(round(self.rate.get())), int(round(self.volume.get())))
        self.voice_status.configure(text="Speaking…", text_color=MUTED)

        def work():
            ok = self.app.speaker.speak(*args)
            msg = ("✓ Sent to your speakers. No sound? Check the Windows volume and output device."
                   if ok else f"✗ Speaker problem: {self.app.speaker.last_error}")
            self.after(0, lambda: self.winfo_exists() and
                       self.voice_status.configure(text=msg, text_color=GREEN if ok else RED))
        threading.Thread(target=work, daemon=True).start()

    def _send_lcd(self):
        text = self.lcd_text.get().strip()
        if not self.app.arduino:
            self.app.show_banner("Connect the Arduino first.", AMBER)
        elif text:
            self.app.arduino.send("A:" + text)

    def save(self):
        c = self.app.cfg
        old = (c["accent"], c["font_size"])
        c["api_key"] = self.key.get().strip()
        c["assistant_name"] = self.name.get().strip() or "Nova"
        c["remember_chat"] = bool(self.remember.get())
        c["quick_prompts"] = [q.strip() for q in self.quick.get("1.0", "end").splitlines() if q.strip()][:8]
        c["model"] = self.model.get()
        c["provider"] = self.provider.get()
        c["ollama_model"] = self.ollama_model.get().strip() or "llama3.2"
        c["ollama_url"] = self.ollama_url.get().strip() or DEFAULT_OLLAMA_URL
        c["stt"] = self.stt.get()
        c["personality"] = self.personality.get()
        c["custom_prompt"] = self.custom.get("1.0", "end").strip()
        c["language"] = self.language.get()
        c["length"] = self.length.get()
        c["speak"] = bool(self.speak.get())
        c["voice"] = self._voice_value()
        c["voice_rate"] = int(round(self.rate.get()))
        c["voice_volume"] = int(round(self.volume.get()))
        c["mic_device"] = "" if self.mic.get() == "Default" else self.mic.get()
        c["mic_sens"] = self.mic_sens.get()
        c["buzzer"] = self.buzzer.get()
        c["clap_sens"] = int(round(self.clap_sens.get()))
        c["show_face"] = bool(self.show_face.get())
        c["theme"] = self.theme.get()
        c["accent"] = self.accent_var.get()
        c["font_size"] = self.font_size.get()
        c["unit"] = self.unit.get()
        c["auto_connect"] = bool(self.auto_connect.get())
        c["clap_enabled"] = bool(self.clap.get())
        c["lcd_answers"] = bool(self.lcd.get())
        c["alert_enabled"] = bool(self.alert.get())
        c["alert_temp"] = int(round(self.alert_temp.get()))
        c["auto_update"] = bool(self.auto_update.get())
        c["update_url"] = self.update_url.get().strip() or DEFAULT_UPDATE_URL
        save_json(CONFIG_FILE, c)
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()
        self.app.on_settings_saved(needs_restart=old != (c["accent"], c["font_size"]))


# ---------------------------------------------------------------- animated face
class Face(ctk.CTkFrame):
    """A small robot face that blinks, follows the mouse and reacts to what the assistant does."""
    CAPTIONS = {"idle": "Click me!", "listening": "I'm listening…", "thinking": "Hmm, let me think…",
                "speaking": "Talking…", "sleepy": "Zzz… clap to wake me", "hot": "Phew, it's hot in here!"}
    MOOD_CAPTIONS = {"happy": "Hehe! 😄", "love": "Aww, I like you too!", "surprised": "Oh!", "dizzy": "Whoaaa…"}

    def __init__(self, master, app, size=180):
        super().__init__(master, fg_color=PANEL, corner_radius=20)
        self.app, self.size = app, size
        self.canvas = tk.Canvas(self, width=size, height=size, highlightthickness=0, bd=0, cursor="hand2")
        self.canvas.pack(padx=14, pady=(16, 2))
        self.caption = ctk.CTkLabel(self, text="", text_color=MUTED, font=(FONT, 13, "bold"))
        self.caption.pack(pady=(0, 14))
        self.state, self.mood, self.mood_until = "idle", None, 0
        self.blink_at = time.time() + 3
        self.active = time.time()
        self.t = 0
        self.pokes = []
        self.canvas.bind("<Button-1>", self.poke)
        self.after(60, self.tick)

    def set_state(self, state):
        self.state = state
        self.active = time.time()

    def react(self, mood, secs=1.6):
        self.mood, self.mood_until = mood, time.time() + secs
        self.active = time.time()

    def poke(self, _e=None):
        now = time.time()
        self.pokes = [p for p in self.pokes if now - p < 1.5] + [now]
        mood = "dizzy" if len(self.pokes) >= 4 else random.choice(["happy", "love", "surprised"])
        self.react(mood, 1.8)
        if self.app.arduino:
            self.app.arduino.send("P:hello")

    def tick(self):
        try:
            self.draw()
        except tk.TclError:
            return
        self.after(50, self.tick)

    @staticmethod
    def col(pair):
        return pair[1] if ctk.get_appearance_mode() == "Dark" else pair[0]

    def draw(self):
        c, S, now = self.canvas, self.size, time.time()
        self.t += 1
        c.delete("all")
        c.configure(bg=self.col(PANEL))
        app = self.app
        mood = self.mood if now < self.mood_until else None
        state = self.state
        hot = bool(app.sensor and app.cfg["alert_enabled"] and app.sensor[0] >= app.cfg["alert_temp"])
        sleepy = state == "idle" and not mood and now - self.active > 90
        shown = mood or ("sleepy" if sleepy else "hot" if hot and state == "idle" else state)
        cap = self.MOOD_CAPTIONS.get(mood) or self.CAPTIONS.get(shown, "")
        if self.caption.cget("text") != cap:
            self.caption.configure(text=cap)

        wobble = math.sin(self.t / 2) * 6 if mood == "dizzy" else 0
        bob = math.sin(self.t / (25 if sleepy else 11)) * 3
        cx, cy, r = S / 2 + wobble, S / 2 + 6 + bob, S * 0.38
        accent = app.accent
        white, dark = "#FFFFFF", "#151722"

        # antenna (blinks while thinking)
        tip = AMBER if state == "thinking" and self.t % 10 < 5 else (RED if hot else accent)
        c.create_line(cx, cy - r, cx, cy - r - 16, fill=shade(accent, 0.7), width=4)
        c.create_oval(cx - 7, cy - r - 26, cx + 7, cy - r - 12, fill=tip, outline="")
        # head + screen
        c.create_oval(cx - r - 9, cy - 10, cx - r + 5, cy + 16, fill=shade(accent, 0.7), outline="")
        c.create_oval(cx + r - 5, cy - 10, cx + r + 9, cy + 16, fill=shade(accent, 0.7), outline="")
        c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=accent, outline="")
        fr = r * 0.8
        c.create_oval(cx - fr, cy - fr * 0.85, cx + fr, cy + fr * 0.9, fill=dark, outline="")

        # eyes: follow the mouse
        ex, ey = r * 0.36, cy - r * 0.14
        ew, eh = r * 0.2, r * 0.26
        try:
            px, py = self.winfo_pointerxy()
            dx, dy = px - (c.winfo_rootx() + cx), py - (c.winfo_rooty() + cy)
        except tk.TclError:
            dx = dy = 0
        dist = max(1.0, math.hypot(dx, dy))
        k = min(1.0, dist / 250)
        lx, ly = dx / dist * k * ew * 0.5, dy / dist * k * eh * 0.45
        if state == "thinking":
            lx, ly = ew * 0.5 * math.cos(self.t / 5), -eh * 0.4
        if now >= self.blink_at + 0.14:
            self.blink_at = now + random.uniform(2.5, 6)
        blinking = now >= self.blink_at
        eye_col = "#7CF0FF" if state == "listening" else white
        for side in (-1, 1):
            x = cx + side * ex
            if mood == "dizzy":
                a = self.t / 2 * side
                for i in range(3):
                    rr = ew * (1 - i * 0.3)
                    c.create_arc(x - rr, ey - rr, x + rr, ey + rr, start=math.degrees(a) + i * 90, extent=250,
                                 style="arc", outline=eye_col, width=2)
            elif mood == "love":
                hs = ew * 0.55
                c.create_oval(x - hs * 1.6, ey - hs, x, ey + hs * 0.4, fill=RED, outline="")
                c.create_oval(x, ey - hs, x + hs * 1.6, ey + hs * 0.4, fill=RED, outline="")
                c.create_polygon(x - hs * 1.55, ey - hs * 0.1, x + hs * 1.55, ey - hs * 0.1, x, ey + hs * 1.5,
                                 fill=RED, outline="")
            elif mood == "happy":
                c.create_arc(x - ew, ey - eh * 0.5, x + ew, ey + eh * 1.1, start=20, extent=140, style="arc",
                             outline=eye_col, width=4)
            elif sleepy or blinking:
                c.create_line(x - ew, ey + 2, x + ew, ey + 2, fill=eye_col, width=4, capstyle="round")
            else:
                h = eh * (1.25 if state == "listening" or mood == "surprised" else 1)
                c.create_oval(x - ew, ey - h, x + ew, ey + h, fill=eye_col, outline="")
                pr = ew * (0.35 if mood == "surprised" else 0.5)
                c.create_oval(x + lx - pr, ey + ly - pr, x + lx + pr, ey + ly + pr, fill=dark, outline="")
                c.create_oval(x + lx - pr * 0.1, ey + ly - pr * 0.75, x + lx + pr * 0.45, ey + ly - pr * 0.2,
                              fill=white, outline="")
        # cheeks
        if mood in ("happy", "love") or hot:
            for side in (-1, 1):
                x = cx + side * ex * 1.45
                c.create_oval(x - 7, ey + eh + 2, x + 7, ey + eh + 10, fill="#FF8FA3", outline="")

        # mouth
        my, mw = cy + r * 0.38, r * 0.3
        if state == "speaking":
            o = 3 + abs(math.sin(self.t / 1.7)) * r * 0.2 * (0.6 + 0.4 * abs(math.sin(self.t / 4.3)))
            c.create_oval(cx - mw * 0.7, my - o / 2, cx + mw * 0.7, my + o / 2, fill=white, outline="")
        elif mood == "surprised" or state == "listening":
            o = 7 + (app.level * 10 if state == "listening" else 0)
            c.create_oval(cx - o, my - o * 0.8, cx + o, my + o * 0.8, outline=white, width=3)
        elif state == "thinking":
            pts = []
            for i in range(9):
                pts += [cx - mw + i * mw / 4, my + math.sin(i + self.t / 3) * 3]
            c.create_line(*pts, fill=white, width=3, smooth=True)
        elif sleepy or mood == "dizzy":
            c.create_oval(cx - 6, my - 4, cx + 6, my + 5, outline=white, width=3)
        elif mood in ("happy", "love"):
            c.create_arc(cx - mw, my - mw * 0.8, cx + mw, my + mw * 0.8, start=200, extent=140, style="chord",
                         fill=white, outline="")
        elif hot:
            c.create_line(cx - mw * 0.8, my + 3, cx - mw * 0.3, my - 2, cx + mw * 0.3, my + 3, cx + mw * 0.8,
                          my - 2, fill=white, width=3, smooth=True)
        else:
            c.create_arc(cx - mw, my - mw * 0.6, cx + mw, my + mw * 0.6, start=200, extent=140, style="arc",
                         outline=white, width=3)

        # extras
        if state == "listening":
            amp = 0.4 + app.level * 1.2
            for i in range(3):
                rr = r + 8 + i * 9 + (self.t % 6) * 1.5 * amp
                for side in (0, 180):
                    c.create_arc(cx - rr, cy - rr, cx + rr, cy + rr, start=side - 25, extent=50, style="arc",
                                 outline=accent, width=2)
        if state == "thinking":
            for i in range(3):
                on = (self.t // 4) % 3 >= i
                c.create_oval(cx + r * 0.55 + i * 12, cy - r - 4 - i * 9, cx + r * 0.55 + i * 12 + 7 + i * 2,
                              cy - r + 3 - i * 9 + i * 2, fill=MUTED[1] if on else self.col(PANEL), outline=MUTED[1])
        if sleepy:
            for i in range(2):
                ph = ((self.t / 30) + i * 0.5) % 1
                c.create_text(cx + r * 0.7 + ph * 18, cy - r * 0.6 - ph * 30, text="z", fill=MUTED[1],
                              font=(FONT, int(10 + ph * 8), "bold"))
        if hot and not mood:
            dy = (self.t % 30) * 0.6
            x0, y0 = cx + r * 0.75, cy - r * 0.45 + dy
            c.create_polygon(x0, y0 - 9, x0 - 6, y0 + 3, x0 + 6, y0 + 3, fill=BLUE, outline="", smooth=True)
            c.create_oval(x0 - 6, y0 - 2, x0 + 6, y0 + 8, fill=BLUE, outline="")


# ---------------------------------------------------------------- main window
class App(ctk.CTk):
    def __init__(self):
        self.cfg = load_config()
        ctk.set_appearance_mode(self.cfg["theme"])
        super().__init__()
        self.accent = ACCENTS.get(self.cfg["accent"], ACCENTS["Violet"])
        self.fs = FONT_SIZES.get(self.cfg["font_size"], 14)
        self.events = queue.Queue()
        self.speaker = Speaker()
        self.arduino = None
        self.busy = False
        self.messages = []          # [(who, text)]
        self.sensor = None
        self.level = 0.0
        self.anim = 0
        self.last_alert = 0
        self.typing = None

        self.title(f"{APP_NAME}  v{APP_VERSION}")
        self.geometry("1260x740")
        self.minsize(980, 600)
        self.configure(fg_color=BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.face_panel = ctk.CTkFrame(self, width=230, fg_color=BG, corner_radius=0)
        self.face_panel.grid_propagate(False)
        self.face = Face(self.face_panel, self)
        self.face.pack(fill="x", padx=(4, 18), pady=(20, 0))
        self._place_face()
        self.recording_stop = False
        self.refresh_ports()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind_all("<Control-space>", lambda e: self.start_voice())
        self.bind_all("<Escape>", lambda e: self.speaker.stop())

        self.after(50, self.poll_events)
        self.after(120, self.animate)
        self._restore_chat()
        if self._needs_key() and not self.cfg["api_key"]:
            self.after(500, self.open_settings)
        saved_ok = any(d == self.cfg["port"] for d, _ in self.ports)
        if self.cfg["auto_connect"] and (saved_ok or guess_port(self.ports, strict=True)):
            self.after(300, self.toggle_connection)
        if self.cfg["auto_update"]:
            self.after(2000, self.check_updates)

    # ---------- layout
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=280, fg_color=PANEL, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        head = ctk.CTkFrame(sb, fg_color="transparent")
        head.pack(fill="x", padx=20, pady=(24, 18))
        self.logo = ctk.CTkLabel(head, text="◉", text_color=self.accent, font=(FONT, 32))
        self.logo.pack(side="left")
        names = ctk.CTkFrame(head, fg_color="transparent")
        names.pack(side="left", padx=10)
        self.title_lbl = ctk.CTkLabel(names, text=self.cfg["assistant_name"], text_color=TEXT,
                                      font=(FONT, 24, "bold"))
        self.title_lbl.pack(anchor="w")
        self.sub_lbl = ctk.CTkLabel(names, text=self._subtitle(),
                                    text_color=MUTED, font=(FONT, 11))
        self.sub_lbl.pack(anchor="w")

        card = ctk.CTkFrame(sb, fg_color=CARD, corner_radius=14)
        card.pack(fill="x", padx=16, pady=6)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(row, text="ARDUINO", text_color=MUTED, font=(FONT, 11, "bold")).pack(side="left")
        self.conn_dot = ctk.CTkLabel(row, text="● Offline", text_color=RED, font=(FONT, 11, "bold"))
        self.conn_dot.pack(side="right")
        prow = ctk.CTkFrame(card, fg_color="transparent")
        prow.pack(fill="x", padx=14, pady=4)
        self.port_menu = ctk.CTkOptionMenu(prow, values=["-"], width=180, fg_color=PANEL, text_color=TEXT,
                                           button_color=PANEL, button_hover_color=AI_BUBBLE)
        self.port_menu.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(prow, text="⟳", width=40, fg_color=PANEL, text_color=TEXT, hover_color=AI_BUBBLE,
                      command=self.refresh_ports).pack(side="right", padx=(6, 0))
        self.conn_btn = ctk.CTkButton(card, text="Connect", height=36, fg_color=self.accent,
                                      hover_color=shade(self.accent), font=(FONT, 13, "bold"),
                                      command=self.toggle_connection)
        self.conn_btn.pack(fill="x", padx=14, pady=(6, 14))

        ctk.CTkLabel(sb, text="ROOM", text_color=MUTED, font=(FONT, 11, "bold")).pack(anchor="w", padx=22, pady=(16, 4))
        grid = ctk.CTkFrame(sb, fg_color="transparent")
        grid.pack(fill="x", padx=16)
        grid.grid_columnconfigure((0, 1), weight=1)
        self.temp_lbl = self._sensor_card(grid, 0, "🌡", "Temperature", f"--°{self.cfg['unit']}", AMBER)
        self.hum_lbl = self._sensor_card(grid, 1, "💧", "Humidity", "--%", BLUE)

        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=16, pady=18)
        self.speak_switch = ctk.CTkSwitch(bottom, text="Speak answers", text_color=TEXT,
                                          progress_color=self.accent, command=self.toggle_speak)
        if self.cfg["speak"]:
            self.speak_switch.select()
        self.speak_switch.pack(anchor="w", pady=6)
        for txt, cmd in (("💾  Export chat", self.export_chat), ("🗑  Clear chat", self.clear_chat),
                         ("⚙  Settings", self.open_settings)):
            ctk.CTkButton(bottom, text=txt, fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                          anchor="w", command=cmd).pack(fill="x", pady=3)
        ctk.CTkLabel(bottom, text="Ctrl+Space = talk · Esc = stop voice", text_color=MUTED,
                     font=(FONT, 10)).pack(anchor="w", pady=(6, 0))

    def _sensor_card(self, parent, col, icon, name, value, color):
        f = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14)
        f.grid(row=0, column=col, sticky="nsew", padx=4)
        ctk.CTkLabel(f, text=icon, font=("Segoe UI Emoji", 20)).pack(anchor="w", padx=12, pady=(10, 0))
        val = ctk.CTkLabel(f, text=value, text_color=color, font=(FONT, 22, "bold"))
        val.pack(anchor="w", padx=12)
        ctk.CTkLabel(f, text=name, text_color=MUTED, font=(FONT, 11)).pack(anchor="w", padx=12, pady=(0, 10))
        return val

    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)
        self.main = main

        top = ctk.CTkFrame(main, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=28, pady=(20, 6))
        ctk.CTkLabel(top, text="Conversation", text_color=TEXT, font=(FONT, 20, "bold")).pack(side="left")
        self.status_lbl = ctk.CTkLabel(top, text="● Ready", text_color=GREEN, font=(FONT, 13, "bold"))
        self.status_lbl.pack(side="right")

        self.banner = ctk.CTkFrame(main, fg_color=CARD, corner_radius=12)
        self.banner_lbl = ctk.CTkLabel(self.banner, text="", text_color=TEXT, font=(FONT, 13), anchor="w")
        self.banner_lbl.pack(side="left", padx=14, pady=8, fill="x", expand=True)
        ctk.CTkButton(self.banner, text="✕", width=30, fg_color="transparent", text_color=MUTED,
                      hover_color=AI_BUBBLE, command=self.hide_banner).pack(side="right", padx=6)
        self.banner_btn = ctk.CTkButton(self.banner, text="", width=110, fg_color=self.accent,
                                        hover_color=shade(self.accent))

        self.chat = ctk.CTkScrollableFrame(main, fg_color=BG, scrollbar_button_color=CARD)
        self.chat.grid(row=2, column=0, sticky="nsew", padx=16)
        self.chat.grid_columnconfigure(0, weight=1)
        self.msg_row = 0

        self.level_bar = ctk.CTkProgressBar(main, height=4, progress_color=self.accent, fg_color=BG)
        self.level_bar.set(0)
        self.level_bar.grid(row=3, column=0, sticky="ew", padx=28)

        self.chips = ctk.CTkFrame(main, fg_color="transparent")
        self.chips.grid(row=4, column=0, sticky="ew", padx=26, pady=(8, 0))
        self._build_chips()

        bar = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=22)
        bar.grid(row=5, column=0, sticky="ew", padx=24, pady=(8, 22))
        bar.grid_columnconfigure(1, weight=1)
        self.mic_btn = ctk.CTkButton(bar, text="🎤", width=52, height=52, corner_radius=26,
                                     fg_color=self.accent, hover_color=shade(self.accent),
                                     font=("Segoe UI Emoji", 22), command=self.start_voice)
        self.mic_btn.grid(row=0, column=0, padx=(10, 8), pady=10)
        self.entry = ctk.CTkEntry(bar, placeholder_text="Type a message, press the mic or clap…",
                                  height=44, border_width=0, fg_color=PANEL, text_color=TEXT,
                                  font=(FONT, self.fs))
        self.entry.grid(row=0, column=1, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.send_text())
        self.stop_btn = ctk.CTkButton(bar, text="⏹", width=44, height=44, corner_radius=18, fg_color=RED,
                                      hover_color=shade(RED), command=self.speaker.stop)
        self.send_btn = ctk.CTkButton(bar, text="Send ➤", width=90, height=44, corner_radius=18,
                                      fg_color=CARD, text_color=TEXT, hover_color=AI_BUBBLE,
                                      font=(FONT, 13, "bold"), command=self.send_text)
        self.send_btn.grid(row=0, column=3, padx=10)

    def _build_chips(self):
        for w in self.chips.winfo_children():
            w.destroy()
        for q in self.cfg["quick_prompts"]:
            ctk.CTkButton(self.chips, text=q, height=28, corner_radius=14, fg_color=CARD, text_color=TEXT,
                          hover_color=AI_BUBBLE, font=(FONT, 12),
                          command=lambda q=q: self.send_text(q)).pack(side="left", padx=4)

    # ---------- banner
    def show_banner(self, text, color=None, action_text=None, action=None):
        self.banner.configure(border_width=2, border_color=color or self.accent)
        self.banner_lbl.configure(text=text)
        if action:
            self.banner_btn.configure(text=action_text, command=action)
            self.banner_btn.pack(side="right", padx=6, before=self.banner_lbl)
        else:
            self.banner_btn.pack_forget()
        self.banner.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 6))

    def hide_banner(self):
        self.banner.grid_forget()

    # ---------- chat
    def add_message(self, who, text, save=True):
        is_user = who == "user"
        wrap = ctk.CTkFrame(self.chat, fg_color="transparent")
        wrap.grid(row=self.msg_row, column=0, sticky="e" if is_user else "w", padx=10, pady=6)
        self.msg_row += 1
        head = ctk.CTkFrame(wrap, fg_color="transparent")
        head.pack(anchor="e" if is_user else "w", padx=6)
        ctk.CTkLabel(head, text=("You" if is_user else self.cfg["assistant_name"]) + "  ·  "
                     + datetime.now().strftime("%H:%M"), text_color=MUTED, font=(FONT, 11, "bold")).pack(side="left")
        if not is_user:
            ctk.CTkButton(head, text="📋", width=24, height=20, fg_color="transparent", hover_color=AI_BUBBLE,
                          command=lambda: (self.clipboard_clear(), self.clipboard_append(text))).pack(side="left")
            ctk.CTkButton(head, text="🔊", width=24, height=20, fg_color="transparent", hover_color=AI_BUBBLE,
                          command=lambda: self._speak_async(text)).pack(side="left")
        ctk.CTkLabel(wrap, text=text, wraplength=560, justify="left", font=(FONT, self.fs),
                     fg_color=self.accent if is_user else AI_BUBBLE, corner_radius=16,
                     text_color="white" if is_user else TEXT).pack(ipadx=12, ipady=8)
        if save:
            self.messages.append((who, text))
            self._save_chat()
        self._scroll_down()
        return wrap

    def _scroll_down(self):
        self.after(60, lambda: self.chat._parent_canvas.yview_moveto(1.0))

    def _show_typing(self, on):
        if on and not self.typing:
            self.typing = ctk.CTkLabel(self.chat, text=f"{self.cfg['assistant_name']} is thinking ●",
                                       text_color=MUTED, font=(FONT, 12, "italic"))
            self.typing.grid(row=self.msg_row, column=0, sticky="w", padx=20, pady=4)
            self.msg_row += 1
            self._scroll_down()
        elif not on and self.typing:
            self.typing.destroy()
            self.typing = None

    def _save_chat(self):
        if self.cfg["remember_chat"]:
            try:
                save_json(CHAT_FILE, self.messages[-200:])
            except OSError:
                pass

    def _restore_chat(self):
        saved = load_json(CHAT_FILE, []) if self.cfg["remember_chat"] else []
        if saved:
            for who, text in saved[-40:]:
                self.add_message(who, text, save=False)
            self.messages = [tuple(m) for m in saved]
        else:
            self.add_message("ai", f"Hi! I'm {self.cfg['assistant_name']}. Press the mic, Ctrl+Space, "
                                   "clap, or type a message.", save=False)

    def clear_chat(self):
        for w in self.chat.winfo_children():
            w.destroy()
        self.msg_row = 0
        self.typing = None
        self.messages.clear()
        self._save_chat()

    def export_chat(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="conversation.txt",
                                            filetypes=[("Text", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                for who, text in self.messages:
                    f.write(f"{'You' if who == 'user' else self.cfg['assistant_name']}: {text}\n\n")
            self.show_banner(f"Chat saved to {os.path.basename(path)}", GREEN)

    def set_status(self, text, color):
        self.status_lbl.configure(text=f"● {text}", text_color=color)
        self.face.set_state({"Listening": "listening", "Thinking": "thinking",
                             "Speaking": "speaking"}.get(text, "idle"))
        if text == "Listening":
            self.mic_btn.configure(state="normal", text="■")
        else:
            self.mic_btn.configure(text="🎤")
            if self.busy:
                self.mic_btn.configure(state="disabled")
        if text == "Speaking":
            self.stop_btn.grid(row=0, column=2, padx=(6, 0))
        else:
            self.stop_btn.grid_forget()
        if self.arduino:
            if text == "Ready" and not self.cfg["lcd_answers"]:
                self.arduino.send("I")
            elif text in ("Listening", "Thinking"):
                self.arduino.send("S:" + text.upper())

    # ---------- arduino
    def refresh_ports(self):
        self.ports = list_ports()
        labels = [l for _, l in self.ports] or ["No ports found"]
        self.port_menu.configure(values=labels)
        want = self.cfg["port"] if any(d == self.cfg["port"] for d, _ in self.ports) else guess_port(self.ports)
        self.port_menu.set(next((l for d, l in self.ports if d == want), labels[0]))

    def toggle_connection(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None
            self._set_conn(False)
            return
        label = self.port_menu.get()
        port = next((d for d, l in self.ports if l == label), None)
        if not port:
            self.show_banner("I can't find the Arduino. Plug it in and press ⟳.", AMBER)
            return
        self.conn_btn.configure(text="Connecting…", state="disabled")

        def work():
            try:
                self.events.put(("connected", (Arduino(port, self.events), port)))
            except Exception as e:
                self.events.put(("connect_failed", str(e)))
        threading.Thread(target=work, daemon=True).start()

    def _set_conn(self, on):
        self.conn_dot.configure(text="● Online" if on else "● Offline", text_color=GREEN if on else RED)
        self.conn_btn.configure(text="Disconnect" if on else "Connect", state="normal",
                                fg_color=CARD if on else self.accent, text_color=TEXT if on else "white")

    def _show_sensor(self, t, h):
        shown = t * 9 / 5 + 32 if self.cfg["unit"] == "F" else t
        self.temp_lbl.configure(text=f"{shown:.1f}°{self.cfg['unit']}",
                                text_color=RED if self.cfg["alert_enabled"] and t >= self.cfg["alert_temp"] else AMBER)
        self.hum_lbl.configure(text=f"{h:.0f}%")
        if self.cfg["alert_enabled"] and t >= self.cfg["alert_temp"] and time.time() - self.last_alert > 600:
            self.last_alert = time.time()
            msg = f"It's getting hot in here: {shown:.0f}°{self.cfg['unit']}!"
            self.show_banner("🔥 " + msg, RED)
            if self.arduino:
                self.arduino.send("A:" + msg)
                self.arduino.send("P:alert")
            if self.cfg["speak"] and not self.busy:
                self._speak_async(msg)

    # ---------- events from threads
    def poll_events(self):
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "connected":
                    self.arduino, port = data
                    self.cfg["port"] = port
                    save_json(CONFIG_FILE, self.cfg)
                    self._set_conn(True)
                    self.arduino.send("I")
                    self._send_arduino_settings()
                    self.face.react("happy")
                elif kind == "connect_failed":
                    self._set_conn(False)
                    hint = " Close the Arduino IDE Serial Monitor first." if "denied" in data.lower() else ""
                    self.show_banner(f"Couldn't connect: {data[:120]}.{hint}", RED)
                elif kind == "disconnected":
                    self.arduino = None
                    self._set_conn(False)
                    self.show_banner("The Arduino was disconnected.", AMBER, "Reconnect", self.toggle_connection)
                elif kind == "sensor":
                    self.sensor = data
                    self._show_sensor(*data)
                elif kind == "clap":
                    st = getattr(self, "_settings", None)
                    if st and st.winfo_exists() and st.monitor.get():
                        st.on_clap()            # testing the sensor: don't start listening
                    elif self.cfg["clap_enabled"]:
                        self.face.react("surprised", 0.8)
                        self.start_voice()
                elif kind == "mic_sensor":
                    st = getattr(self, "_settings", None)
                    if st and st.winfo_exists():
                        st.on_mic_sensor(*data)
                elif kind == "status":
                    self.set_status(*data)
                elif kind == "typing":
                    self._show_typing(data)
                elif kind == "message":
                    self._show_typing(False)
                    self.add_message(*data)
                    if data[0] == "ai":
                        self.face.react("happy", 1.2)
                elif kind == "level":
                    self.level = data
                elif kind == "banner":
                    self.show_banner(*data)
                elif kind == "done":
                    self.busy = False
                    self.level = 0
                    self._show_typing(False)
                    self.mic_btn.configure(state="normal")
                    self.send_btn.configure(state="normal")
                    self.set_status("Ready", GREEN)
        except queue.Empty:
            pass
        self.after(50, self.poll_events)

    def animate(self):
        self.anim += 1
        self.level_bar.set(min(1.0, self.level))
        listening = self.busy and self.status_lbl.cget("text").endswith("Listening")
        if listening:
            self.mic_btn.configure(fg_color=RED if self.anim % 2 else shade(RED))
        elif not self.busy:
            self.mic_btn.configure(fg_color=self.accent)
        if self.typing:
            self.typing.configure(text=f"{self.cfg['assistant_name']} is thinking " + "●" * (self.anim % 3 + 1))
        self.after(250, self.animate)

    # ---------- actions
    def toggle_speak(self):
        self.cfg["speak"] = bool(self.speak_switch.get())
        save_json(CONFIG_FILE, self.cfg)
        if not self.cfg["speak"]:
            self.speaker.stop()

    def open_settings(self):
        if getattr(self, "_settings", None) and self._settings.winfo_exists():
            self._settings.lift()
            return
        self._settings = SettingsWindow(self)

    def _send_arduino_settings(self):
        if self.arduino:
            self.arduino.send(f"B:{BUZZER_MODES.index(self.cfg['buzzer']) if self.cfg['buzzer'] in BUZZER_MODES else 2}")
            self.arduino.send(f"K:{self.cfg['clap_sens']}")

    def _place_face(self):
        if self.cfg["show_face"]:
            self.face_panel.grid(row=0, column=2, sticky="nsew")
        else:
            self.face_panel.grid_forget()

    def on_settings_saved(self, needs_restart=False):
        ctk.set_appearance_mode(self.cfg["theme"])
        self._send_arduino_settings()
        self._place_face()
        self.title_lbl.configure(text=self.cfg["assistant_name"])
        self.sub_lbl.configure(text=self._subtitle())
        if self.cfg["speak"]:
            self.speak_switch.select()
        else:
            self.speak_switch.deselect()
        self._build_chips()
        if self.sensor:
            self._show_sensor(*self.sensor)
        if needs_restart:
            self.show_banner("Restart to apply the new colour / text size.", self.accent,
                             "Restart now", self.restart)
        else:
            self.show_banner("Settings saved ✓", GREEN)
            self.after(2500, self.hide_banner)

    def restart(self):
        restart_app()
        self.on_close()

    def check_updates(self, manual=False):
        def work():
            try:
                info = check_for_update(self.cfg["update_url"])
            except Exception as e:
                if manual:
                    self.events.put(("banner", (f"Couldn't check for updates: {str(e)[:100]}", AMBER)))
                return
            if not info:
                if manual:
                    self.events.put(("banner", (f"You have the latest version ({APP_VERSION}).", GREEN)))
                return
            notes = info.get("notes", "")
            if info.get("manual"):
                self.events.put(("banner", (f"Version {info['version']} is on GitHub. {notes}", self.accent)))
            else:
                self.events.put(("banner", (f"Updated to {info['version']}! {notes}", GREEN,
                                            "Restart now", self.restart)))
        threading.Thread(target=work, daemon=True).start()

    def _speak(self, text):
        ok = self.speaker.speak(text, self.cfg["voice"], self.cfg["voice_rate"], self.cfg["voice_volume"],
                                speech_lang(text, self.cfg["language"]))
        if not ok:
            self.events.put(("banner", (f"🔇 Speaker problem: {self.speaker.last_error}", RED,
                                        "Voice settings", self.open_settings)))
        return ok

    def _speak_async(self, text):
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _local(self):
        return self.cfg["provider"] == PROVIDERS[1]

    def _needs_key(self):
        return not self._local() or self.cfg["stt"] == STT_ENGINES[0]

    def _subtitle(self):
        model = ("🖥 " + self.cfg["ollama_model"]) if self._local() else self.cfg["model"]
        if len(model) > 22:
            model = model[:21] + "…"
        return f"{self.cfg['personality']} · {model} · v{APP_VERSION}"

    def _ready_to_ask(self, voice=False):
        if self.busy:
            return False
        needs_key = not self._local() or (voice and self.cfg["stt"] == STT_ENGINES[0])
        if needs_key and not self.cfg["api_key"]:
            self.show_banner("Add a Groq API key in Settings, or switch to Ollama + Windows speech.",
                             AMBER, "Open", self.open_settings)
            return False
        self.speaker.stop()
        self.busy = True
        self.mic_btn.configure(state="disabled")
        self.send_btn.configure(state="disabled")
        return True

    def start_voice(self):
        if self.busy and self.status_lbl.cget("text").endswith("Listening"):
            self.recording_stop = True          # pressing the mic again = "I'm done talking"
            return
        if self._ready_to_ask(voice=True):
            self.recording_stop = False
            threading.Thread(target=self._voice_worker, daemon=True).start()

    def send_text(self, text=None):
        text = (text or self.entry.get()).strip()
        if text and self._ready_to_ask():
            self.entry.delete(0, "end")
            self.add_message("user", text)
            threading.Thread(target=self._ask_worker, args=(text,), daemon=True).start()

    # ---------- background work
    def _record(self):
        return record_speech(self.cfg["mic_device"], self.cfg["mic_sens"],
                             on_level=lambda v: self.events.put(("level", v)),
                             should_stop=lambda: self.recording_stop)

    def _voice_worker(self):
        try:
            self.events.put(("status", ("Listening", RED)))
            try:
                wav, info = self._record()
            except Exception as e:
                self.events.put(("banner", (f"Microphone problem: {e}. Pick your mic in Settings > Voice.", RED,
                                            "Settings", self.open_settings)))
                return
            self.events.put(("level", 0))
            if not wav:
                if info.get("problem") == "silent":
                    msg = ("Your microphone gives no sound. Pick the right mic in Settings > Voice and allow "
                           "desktop apps to use the microphone in Windows privacy settings.")
                else:
                    msg = "I didn't hear any words. Talk a bit closer, or set Mic sensitivity to High."
                self.events.put(("banner", (msg, AMBER, "Settings", self.open_settings)))
                return
            self.events.put(("status", ("Thinking", AMBER)))
            lang = LANGUAGES.get(self.cfg["language"])
            if self.cfg["stt"] == STT_ENGINES[1]:
                text = windows_stt(wav, lang)
            else:
                kwargs = {"language": lang} if lang else {}
                text = Groq(api_key=self.cfg["api_key"]).audio.transcriptions.create(
                    file=("q.wav", wav), model=STT_MODEL, **kwargs).text.strip()
            if not text:
                self.events.put(("banner", ("Sorry, I couldn't understand that.", AMBER)))
                return
            self.events.put(("message", ("user", text)))
            self._answer(text)
        except Exception as e:
            self.events.put(("message", ("ai", self._friendly_error(e))))
        finally:
            self.events.put(("done", None))

    def _ask_worker(self, text):
        try:
            self._answer(text)
        except Exception as e:
            self.events.put(("message", ("ai", self._friendly_error(e))))
        finally:
            self.events.put(("done", None))

    def _system_prompt(self):
        c = self.cfg
        length_txt, _ = LENGTHS.get(c["length"], LENGTHS["Short"])
        parts = [f"You are {c['assistant_name']}, a voice assistant inside a small Arduino gadget "
                 "with a 16x2 LCD screen.", PERSONALITIES.get(c["personality"], "")]
        if c["custom_prompt"]:
            parts.append(c["custom_prompt"])
        lang = c["language"]
        parts.append("Reply in the user's language." if lang == "Auto" else f"Always reply in {lang}.")
        parts.append(f"Answer in {length_txt}, plain text, no emojis or markdown.")
        parts.append("Current date and time: " + datetime.now().strftime("%A %d %B %Y, %H:%M") + ".")
        if self.sensor:
            t, h = self.sensor
            parts.append(f"A sensor in the room reads {t:.1f} C ({t * 9 / 5 + 32:.0f} F) and {h:.0f}% "
                         f"humidity; the user prefers degrees {c['unit']}. Use it when asked about the room.")
        else:
            parts.append("No room sensor data is available right now.")
        return " ".join(p for p in parts if p)

    def _answer(self, question):
        self.events.put(("status", ("Thinking", AMBER)))
        self.events.put(("typing", True))
        history = [{"role": "user" if w == "user" else "assistant", "content": t}
                   for w, t in self.messages[-12:]]
        if not history or history[-1]["content"] != question:
            history.append({"role": "user", "content": question})
        _, max_tokens = LENGTHS.get(self.cfg["length"], LENGTHS["Short"])
        messages = [{"role": "system", "content": self._system_prompt()}] + history
        if self._local():
            reply = ollama_chat(self.cfg["ollama_url"], self.cfg["ollama_model"], messages, max_tokens)
        else:
            reply = Groq(api_key=self.cfg["api_key"]).chat.completions.create(
                model=self.cfg["model"], messages=messages, max_tokens=max_tokens,
            ).choices[0].message.content.strip()
        if not reply:
            reply = "Hmm, I don't have an answer for that."
        self.events.put(("message", ("ai", reply)))
        if self.arduino and self.cfg["lcd_answers"]:
            self.arduino.send("A:" + reply)
        if self.cfg["speak"]:
            self.events.put(("status", ("Speaking", self.accent)))
            self._speak(reply)

    @staticmethod
    def _friendly_error(e):
        msg = str(e)
        low = msg.lower()
        if msg == "OLLAMA_OFFLINE":
            return "Ollama isn't running. Install it from ollama.com and open it (it sits in the tray)."
        if msg.startswith("OLLAMA_NO_MODEL:"):
            m = msg.split(":", 1)[1]
            return f"The model '{m}' isn't installed. Open cmd and run:  ollama pull {m}"
        if msg.startswith("WIN_STT:") or "recognizer" in low:
            return ("Windows speech recognition didn't work. Add a speech language in Windows Settings > "
                    "Time & language > Speech, or switch to Groq Whisper in ⚙ Settings > Voice.")
        if "401" in msg or "invalid_api_key" in low:
            return "Your API key doesn't work. Check it in ⚙ Settings."
        if "connect" in low or "timeout" in low:
            return "I can't reach the internet right now. Check your connection."
        if "429" in msg:
            return "Too many requests - wait a few seconds and try again."
        return f"Something went wrong: {msg[:200]}"

    def on_close(self):
        self.speaker.stop()
        if self.arduino:
            self.arduino.close()
        self.destroy()


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
