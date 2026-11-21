"""
AI Assistant - Windows desktop app for the Arduino LCD voice assistant.

Talk with the mic button, Ctrl+Space, a clap on the KY-037, or type.
Answers are spoken, shown in the chat and scrolled on the 16x2 LCD.
Live DHT11 readings are shown in the sidebar and given to the AI.
The app updates itself from GitHub when started through launcher.py / the exe.
"""
import io
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import wave
from datetime import datetime
from tkinter import filedialog

import customtkinter as ctk
import numpy as np
import serial
import serial.tools.list_ports
import sounddevice as sd
from groq import Groq
from unidecode import unidecode

APP_NAME = "AI Assistant"
APP_VERSION = "2.0.0"

SAMPLE_RATE = 16000
STT_MODEL = "whisper-large-v3-turbo"
CHAT_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
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
    "assistant_name": "Nova", "personality": "Friendly", "custom_prompt": "",
    "language": "Auto", "length": "Short",
    "speak": True, "voice": "", "voice_rate": 1, "voice_volume": 100,
    "silence_level": 500, "clap_enabled": True, "lcd_answers": True,
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


# ---------------------------------------------------------------- speech out
class Speaker:
    def __init__(self):
        self.proc = None

    def speak(self, text, voice="", rate=1, volume=100):
        if IS_WIN:
            fd, path = tempfile.mkstemp(suffix=".txt")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
            voice_cmd = ""
            if voice:
                voice_cmd = "try { $s.SelectVoice('%s') } catch {}; " % voice.replace("'", "''")
            ps = ("Add-Type -AssemblyName System.Speech; "
                  "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                  f"{voice_cmd}$s.Rate = {int(rate)}; $s.Volume = {int(volume)}; "
                  f"$s.Speak((Get-Content -Raw -Encoding UTF8 '{path}'))")
            try:
                self.proc = subprocess.Popen(["powershell", "-NoProfile", "-Command", ps],
                                             creationflags=NO_WINDOW)
                self.proc.wait()
            finally:
                self.proc = None
                try:
                    os.remove(path)
                except OSError:
                    pass
        else:
            try:
                import pyttsx3
                e = pyttsx3.init()
                e.say(text)
                e.runAndWait()
            except Exception:
                pass

    def stop(self):
        p = self.proc
        if p and p.poll() is None:
            p.kill()

    @staticmethod
    def list_voices():
        if not IS_WIN:
            return []
        ps = ("Add-Type -AssemblyName System.Speech; "
              "(New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() | "
              "% { $_.VoiceInfo.Name }")
        try:
            out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True,
                                 text=True, timeout=20, creationflags=NO_WINDOW).stdout
            return [v.strip() for v in out.splitlines() if v.strip()]
        except Exception:
            return []


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
        self._label(p, "Groq API key", "Free at console.groq.com - stored only on this PC")
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
        self._label(p, "Model", "70b = smartest, 8b = fastest")
        self.model = self._menu(p, CHAT_MODELS, cfg["model"])
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
                      command=self._test_voice).pack(anchor="w", pady=8)
        self._label(p, "Microphone silence level", "Raise it if recording never stops in a noisy room")
        self.silence = self._slider(p, 100, 2000, cfg["silence_level"])

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

        # ----- Arduino
        p = pages["Arduino"]
        self.auto_connect = self._switch(p, "Connect automatically at startup", cfg["auto_connect"])
        self.clap = self._switch(p, "Clap to talk (KY-037 sound sensor)", cfg["clap_enabled"])
        self.lcd = self._switch(p, "Show answers on the LCD", cfg["lcd_answers"])
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
        s.set(value)
        s.pack(side="left", fill="x", expand=True)
        return s

    def _load_voices(self):
        voices = Speaker.list_voices()
        if voices:
            self.after(0, lambda: self.voice.configure(values=["Default"] + voices))

    def _voice_value(self):
        v = self.voice.get()
        return "" if v == "Default" else v

    def _test_voice(self):
        text = f"Hi, I'm {self.name.get().strip() or 'Nova'}. This is how I sound."
        args = (text, self._voice_value(), int(round(self.rate.get())), int(round(self.volume.get())))
        threading.Thread(target=self.app.speaker.speak, args=args, daemon=True).start()

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
        c["personality"] = self.personality.get()
        c["custom_prompt"] = self.custom.get("1.0", "end").strip()
        c["language"] = self.language.get()
        c["length"] = self.length.get()
        c["speak"] = bool(self.speak.get())
        c["voice"] = self._voice_value()
        c["voice_rate"] = int(round(self.rate.get()))
        c["voice_volume"] = int(round(self.volume.get()))
        c["silence_level"] = int(self.silence.get())
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
        self.geometry("1080x720")
        self.minsize(860, 580)
        self.configure(fg_color=BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.refresh_ports()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind_all("<Control-space>", lambda e: self.start_voice())
        self.bind_all("<Escape>", lambda e: self.speaker.stop())

        self.after(50, self.poll_events)
        self.after(120, self.animate)
        self._restore_chat()
        if not self.cfg["api_key"]:
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
        self.sub_lbl = ctk.CTkLabel(names, text=f"{self.cfg['personality']} · v{APP_VERSION}",
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
                    if self.cfg["clap_enabled"]:
                        self.start_voice()
                elif kind == "status":
                    self.set_status(*data)
                elif kind == "typing":
                    self._show_typing(data)
                elif kind == "message":
                    self._show_typing(False)
                    self.add_message(*data)
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

    def on_settings_saved(self, needs_restart=False):
        ctk.set_appearance_mode(self.cfg["theme"])
        self.title_lbl.configure(text=self.cfg["assistant_name"])
        self.sub_lbl.configure(text=f"{self.cfg['personality']} · v{APP_VERSION}")
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

    def _speak_async(self, text):
        threading.Thread(target=self.speaker.speak, args=(text, self.cfg["voice"], self.cfg["voice_rate"],
                                                          self.cfg["voice_volume"]), daemon=True).start()

    def _ready_to_ask(self):
        if self.busy:
            return False
        if not self.cfg["api_key"]:
            self.show_banner("Add your Groq API key in Settings first.", AMBER, "Open", self.open_settings)
            return False
        self.speaker.stop()
        self.busy = True
        self.mic_btn.configure(state="disabled")
        self.send_btn.configure(state="disabled")
        return True

    def start_voice(self):
        if self._ready_to_ask():
            threading.Thread(target=self._voice_worker, daemon=True).start()

    def send_text(self, text=None):
        text = (text or self.entry.get()).strip()
        if text and self._ready_to_ask():
            self.entry.delete(0, "end")
            self.add_message("user", text)
            threading.Thread(target=self._ask_worker, args=(text,), daemon=True).start()

    # ---------- background work
    def _record(self):
        frames, spoke, quiet_since = [], False, None
        start = time.time()
        silence = self.cfg["silence_level"]
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
            while time.time() - start < MAX_SECONDS:
                block, _ = stream.read(1600)
                frames.append(block)
                vol = float(np.abs(block).mean())
                self.events.put(("level", vol / (silence * 4)))
                if vol > silence:
                    spoke, quiet_since = True, None
                elif spoke:
                    quiet_since = quiet_since or time.time()
                    if time.time() - quiet_since > 1.2:
                        break
                elif time.time() - start > 6:
                    return None
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(np.concatenate(frames).tobytes())
        return buf.getvalue()

    def _voice_worker(self):
        try:
            self.events.put(("status", ("Listening", RED)))
            try:
                wav = self._record()
            except Exception as e:
                self.events.put(("banner", (f"Microphone problem: {e}", RED)))
                return
            self.events.put(("level", 0))
            if not wav:
                self.events.put(("banner", ("I didn't hear anything. Try again a bit louder.", AMBER)))
                return
            self.events.put(("status", ("Thinking", AMBER)))
            kwargs = {}
            if LANGUAGES.get(self.cfg["language"]):
                kwargs["language"] = LANGUAGES[self.cfg["language"]]
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
        reply = Groq(api_key=self.cfg["api_key"]).chat.completions.create(
            model=self.cfg["model"],
            messages=[{"role": "system", "content": self._system_prompt()}] + history,
            max_tokens=max_tokens,
        ).choices[0].message.content.strip()
        self.events.put(("message", ("ai", reply)))
        if self.arduino and self.cfg["lcd_answers"]:
            self.arduino.send("A:" + reply)
        if self.cfg["speak"]:
            self.events.put(("status", ("Speaking", self.accent)))
            self.speaker.speak(reply, self.cfg["voice"], self.cfg["voice_rate"], self.cfg["voice_volume"])

    @staticmethod
    def _friendly_error(e):
        msg = str(e)
        low = msg.lower()
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
