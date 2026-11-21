"""
AI Assistant - Windows desktop app for the Arduino LCD voice assistant.

Talk with the mic button, a clap on the KY-037, or type. Answers are spoken,
shown in the chat and scrolled on the 16x2 LCD. Live DHT11 readings are shown
in the sidebar and given to the AI.
"""
import io
import json
import os
import queue
import subprocess
import sys
import threading
import time
import wave

import customtkinter as ctk
import numpy as np
import serial
import serial.tools.list_ports
import sounddevice as sd
from groq import Groq
from unidecode import unidecode

APP_NAME = "AI Assistant"
SAMPLE_RATE = 16000
STT_MODEL = "whisper-large-v3-turbo"
CHAT_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
MAX_SECONDS = 12

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "AIAssistant")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DEFAULTS = {
    "api_key": "", "port": "", "model": CHAT_MODELS[0], "speak": True,
    "voice_rate": 1, "silence_level": 500, "assistant_name": "Nova",
}

ACCENT = "#7C5CFF"
ACCENT_HOVER = "#6847F5"
BG = "#0F1117"
PANEL = "#171A23"
CARD = "#1F2330"
USER_BUBBLE = "#7C5CFF"
AI_BUBBLE = "#252A38"
MUTED = "#8A90A6"
GREEN, RED, AMBER = "#3DDC97", "#FF5C7A", "#FFB547"


# ---------------------------------------------------------------- config
def load_config():
    cfg = dict(DEFAULTS)
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    if not cfg["api_key"]:
        cfg["api_key"] = os.environ.get("GROQ_API_KEY", "")
    return cfg


def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


# ---------------------------------------------------------------- speech out
def speak(text, rate=1):
    """Speak with the built-in Windows voice (no extra install needed)."""
    if sys.platform == "win32":
        safe = text.replace("'", "''")
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"$s.Rate = {int(rate)}; $s.Speak('{safe}')")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       creationflags=0x08000000)  # CREATE_NO_WINDOW
    else:
        try:
            import pyttsx3
            e = pyttsx3.init()
            e.say(text)
            e.runAndWait()
        except Exception:
            pass


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
            except (serial.SerialException, OSError):
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
        self.alive = False
        try:
            self.send("I")
            self.ser.close()
        except Exception:
            pass


def list_ports():
    out = []
    for p in serial.tools.list_ports.comports():
        out.append((p.device, f"{p.device} - {p.description}"))
    return out


def guess_port(ports):
    for dev, label in ports:
        if any(k in label.lower() for k in ("arduino", "ch340", "ch341", "usb-serial", "usb serial")):
            return dev
    return ports[0][0] if ports else ""


# ---------------------------------------------------------------- settings window
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Settings")
        self.geometry("460x520")
        self.configure(fg_color=PANEL)
        self.resizable(False, False)
        self.transient(app)
        self.after(100, self.grab_set)
        cfg = app.cfg

        ctk.CTkLabel(self, text="Settings", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 10))

        def field(label, hint=None):
            ctk.CTkLabel(self, text=label, font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=24, pady=(10, 2))
            if hint:
                ctk.CTkLabel(self, text=hint, text_color=MUTED, font=("Segoe UI", 11)).pack(anchor="w", padx=24)

        field("Groq API key", "Free at console.groq.com - stored only on this PC")
        self.key = ctk.CTkEntry(self, width=410, show="•", height=36)
        self.key.insert(0, cfg["api_key"])
        self.key.pack(padx=24, pady=4)

        field("Assistant name")
        self.name = ctk.CTkEntry(self, width=410, height=36)
        self.name.insert(0, cfg["assistant_name"])
        self.name.pack(padx=24, pady=4)

        field("AI model", "70b = smartest, 8b = fastest")
        self.model = ctk.CTkOptionMenu(self, values=CHAT_MODELS, width=410, fg_color=CARD,
                                       button_color=ACCENT, button_hover_color=ACCENT_HOVER)
        self.model.set(cfg["model"])
        self.model.pack(padx=24, pady=4)

        field("Voice speed")
        self.rate = ctk.CTkSlider(self, from_=-5, to=5, number_of_steps=10, width=410,
                                  button_color=ACCENT, progress_color=ACCENT)
        self.rate.set(cfg["voice_rate"])
        self.rate.pack(padx=24, pady=6)

        field("Silence level", "Raise it if recording never stops in a noisy room")
        self.silence = ctk.CTkSlider(self, from_=100, to=2000, width=410,
                                     button_color=ACCENT, progress_color=ACCENT)
        self.silence.set(cfg["silence_level"])
        self.silence.pack(padx=24, pady=6)

        ctk.CTkButton(self, text="Save", height=40, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=("Segoe UI", 14, "bold"), command=self.save).pack(fill="x", padx=24, pady=20)

    def save(self):
        c = self.app.cfg
        c["api_key"] = self.key.get().strip()
        c["assistant_name"] = self.name.get().strip() or "Nova"
        c["model"] = self.model.get()
        c["voice_rate"] = int(round(self.rate.get()))
        c["silence_level"] = int(self.silence.get())
        save_config(c)
        self.app.on_settings_saved()
        self.destroy()


# ---------------------------------------------------------------- main window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.cfg = load_config()
        self.events = queue.Queue()
        self.arduino = None
        self.busy = False
        self.history = []
        self.sensor = None
        self.level = 0.0
        self.anim = 0

        self.title(APP_NAME)
        self.geometry("1000x680")
        self.minsize(820, 560)
        self.configure(fg_color=BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.refresh_ports()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Return>", lambda e: self.send_text())

        self.after(50, self.poll_events)
        self.after(120, self.animate)
        self.add_message("ai", f"Hi! I'm {self.cfg['assistant_name']}. Connect your Arduino, "
                               "then press the mic, clap, or type a message.")
        if not self.cfg["api_key"]:
            self.after(400, self.open_settings)

    # ---------- layout
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=270, fg_color=PANEL, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        head = ctk.CTkFrame(sb, fg_color="transparent")
        head.pack(fill="x", padx=20, pady=(24, 18))
        ctk.CTkLabel(head, text="◉", text_color=ACCENT, font=("Segoe UI", 30)).pack(side="left")
        self.title_lbl = ctk.CTkLabel(head, text=self.cfg["assistant_name"], font=("Segoe UI", 24, "bold"))
        self.title_lbl.pack(side="left", padx=10)

        # connection card
        card = ctk.CTkFrame(sb, fg_color=CARD, corner_radius=14)
        card.pack(fill="x", padx=16, pady=6)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(row, text="ARDUINO", text_color=MUTED, font=("Segoe UI", 11, "bold")).pack(side="left")
        self.conn_dot = ctk.CTkLabel(row, text="● Offline", text_color=RED, font=("Segoe UI", 11, "bold"))
        self.conn_dot.pack(side="right")

        prow = ctk.CTkFrame(card, fg_color="transparent")
        prow.pack(fill="x", padx=14, pady=4)
        self.port_menu = ctk.CTkOptionMenu(prow, values=["-"], width=170, fg_color=BG,
                                           button_color=BG, button_hover_color=AI_BUBBLE)
        self.port_menu.pack(side="left")
        ctk.CTkButton(prow, text="⟳", width=40, fg_color=BG, hover_color=AI_BUBBLE,
                      command=self.refresh_ports).pack(side="right")
        self.conn_btn = ctk.CTkButton(card, text="Connect", height=36, fg_color=ACCENT,
                                      hover_color=ACCENT_HOVER, font=("Segoe UI", 13, "bold"),
                                      command=self.toggle_connection)
        self.conn_btn.pack(fill="x", padx=14, pady=(6, 14))

        # sensor cards
        ctk.CTkLabel(sb, text="ROOM", text_color=MUTED, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=22, pady=(16, 4))
        grid = ctk.CTkFrame(sb, fg_color="transparent")
        grid.pack(fill="x", padx=16)
        grid.grid_columnconfigure((0, 1), weight=1)
        self.temp_lbl = self._sensor_card(grid, 0, "🌡", "Temperature", "--°C", AMBER)
        self.hum_lbl = self._sensor_card(grid, 1, "💧", "Humidity", "--%", "#4FC3F7")

        # bottom buttons
        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=16, pady=18)
        self.speak_switch = ctk.CTkSwitch(bottom, text="Speak answers", progress_color=ACCENT,
                                          command=self.toggle_speak)
        if self.cfg["speak"]:
            self.speak_switch.select()
        self.speak_switch.pack(anchor="w", pady=6)
        ctk.CTkButton(bottom, text="🗑  Clear chat", fg_color=CARD, hover_color=AI_BUBBLE, anchor="w",
                      command=self.clear_chat).pack(fill="x", pady=3)
        ctk.CTkButton(bottom, text="⚙  Settings", fg_color=CARD, hover_color=AI_BUBBLE, anchor="w",
                      command=self.open_settings).pack(fill="x", pady=3)

    def _sensor_card(self, parent, col, icon, name, value, color):
        f = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14)
        f.grid(row=0, column=col, sticky="nsew", padx=4)
        ctk.CTkLabel(f, text=icon, font=("Segoe UI Emoji", 20)).pack(anchor="w", padx=12, pady=(10, 0))
        val = ctk.CTkLabel(f, text=value, text_color=color, font=("Segoe UI", 22, "bold"))
        val.pack(anchor="w", padx=12)
        ctk.CTkLabel(f, text=name, text_color=MUTED, font=("Segoe UI", 11)).pack(anchor="w", padx=12, pady=(0, 10))
        return val

    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(main, fg_color="transparent", height=60)
        top.grid(row=0, column=0, sticky="ew", padx=28, pady=(20, 6))
        ctk.CTkLabel(top, text="Conversation", font=("Segoe UI", 20, "bold")).pack(side="left")
        self.status_lbl = ctk.CTkLabel(top, text="● Ready", text_color=GREEN, font=("Segoe UI", 13, "bold"))
        self.status_lbl.pack(side="right")

        self.chat = ctk.CTkScrollableFrame(main, fg_color=BG, scrollbar_button_color=CARD)
        self.chat.grid(row=1, column=0, sticky="nsew", padx=16)
        self.chat.grid_columnconfigure(0, weight=1)
        self.msg_row = 0

        # voice level bar
        self.level_bar = ctk.CTkProgressBar(main, height=4, progress_color=ACCENT, fg_color=BG)
        self.level_bar.set(0)
        self.level_bar.grid(row=2, column=0, sticky="ew", padx=28)

        bar = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=22)
        bar.grid(row=3, column=0, sticky="ew", padx=24, pady=(8, 22))
        bar.grid_columnconfigure(1, weight=1)
        self.mic_btn = ctk.CTkButton(bar, text="🎤", width=52, height=52, corner_radius=26,
                                     fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                     font=("Segoe UI Emoji", 22), command=self.start_voice)
        self.mic_btn.grid(row=0, column=0, padx=(10, 8), pady=10)
        self.entry = ctk.CTkEntry(bar, placeholder_text="Type a message or press the mic…",
                                  height=44, border_width=0, fg_color=PANEL, font=("Segoe UI", 14))
        self.entry.grid(row=0, column=1, sticky="ew")
        self.send_btn = ctk.CTkButton(bar, text="Send ➤", width=90, height=44, corner_radius=18,
                                      fg_color=CARD, hover_color=AI_BUBBLE, font=("Segoe UI", 13, "bold"),
                                      command=self.send_text)
        self.send_btn.grid(row=0, column=2, padx=10)

    # ---------- chat helpers
    def add_message(self, who, text):
        is_user = who == "user"
        wrap = ctk.CTkFrame(self.chat, fg_color="transparent")
        wrap.grid(row=self.msg_row, column=0, sticky="e" if is_user else "w", padx=10, pady=6)
        self.msg_row += 1
        ctk.CTkLabel(wrap, text="You" if is_user else self.cfg["assistant_name"], text_color=MUTED,
                     font=("Segoe UI", 11, "bold")).pack(anchor="e" if is_user else "w", padx=6)
        ctk.CTkLabel(wrap, text=text, wraplength=520, justify="left", font=("Segoe UI", 14),
                     fg_color=USER_BUBBLE if is_user else AI_BUBBLE, corner_radius=16,
                     text_color="white").pack(ipadx=12, ipady=8)
        self.after(60, lambda: self.chat._parent_canvas.yview_moveto(1.0))

    def clear_chat(self):
        for w in self.chat.winfo_children():
            w.destroy()
        self.msg_row = 0
        self.history.clear()

    def set_status(self, text, color):
        self.status_lbl.configure(text=f"● {text}", text_color=color)
        if self.arduino:
            if text == "Ready":
                self.arduino.send("I")
            elif text in ("Listening", "Thinking"):
                self.arduino.send("S:" + text.upper())

    # ---------- arduino
    def refresh_ports(self):
        self.ports = list_ports()
        labels = [l for _, l in self.ports] or ["No ports found"]
        self.port_menu.configure(values=labels)
        want = self.cfg["port"] if any(d == self.cfg["port"] for d, _ in self.ports) else guess_port(self.ports)
        for d, l in self.ports:
            if d == want:
                self.port_menu.set(l)
                return
        self.port_menu.set(labels[0])

    def toggle_connection(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None
            self._set_conn(False)
            return
        label = self.port_menu.get()
        port = next((d for d, l in self.ports if l == label), None)
        if not port:
            self.add_message("ai", "I can't find the Arduino. Plug it in and press ⟳.")
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
                                fg_color=CARD if on else ACCENT)

    # ---------- events from threads
    def poll_events(self):
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "connected":
                    self.arduino, port = data
                    self.cfg["port"] = port
                    save_config(self.cfg)
                    self._set_conn(True)
                    self.arduino.send("I")
                elif kind == "connect_failed":
                    self._set_conn(False)
                    hint = " Close the Arduino IDE Serial Monitor first." if "denied" in data.lower() else ""
                    self.add_message("ai", f"Couldn't connect: {data}.{hint}")
                elif kind == "disconnected":
                    self.arduino = None
                    self._set_conn(False)
                    self.add_message("ai", "The Arduino was disconnected.")
                elif kind == "sensor":
                    self.sensor = data
                    self.temp_lbl.configure(text=f"{data[0]:.1f}°C")
                    self.hum_lbl.configure(text=f"{data[1]:.0f}%")
                elif kind == "clap":
                    self.start_voice()
                elif kind == "status":
                    self.set_status(*data)
                elif kind == "message":
                    self.add_message(*data)
                elif kind == "level":
                    self.level = data
                elif kind == "done":
                    self.busy = False
                    self.level = 0
                    self.mic_btn.configure(state="normal")
                    self.send_btn.configure(state="normal")
                    self.set_status("Ready", GREEN)
        except queue.Empty:
            pass
        self.after(50, self.poll_events)

    def animate(self):
        self.anim += 1
        self.level_bar.set(min(1.0, self.level))
        if self.busy and self.status_lbl.cget("text").endswith("Listening"):
            self.mic_btn.configure(fg_color=RED if self.anim % 2 else "#E0435F")
        elif not self.busy:
            self.mic_btn.configure(fg_color=ACCENT)
        self.after(250, self.animate)

    # ---------- actions
    def toggle_speak(self):
        self.cfg["speak"] = bool(self.speak_switch.get())
        save_config(self.cfg)

    def open_settings(self):
        SettingsWindow(self)

    def on_settings_saved(self):
        self.title_lbl.configure(text=self.cfg["assistant_name"])

    def _ready_to_ask(self):
        if self.busy:
            return False
        if not self.cfg["api_key"]:
            self.add_message("ai", "Please add your Groq API key in ⚙ Settings first.")
            self.open_settings()
            return False
        self.busy = True
        self.mic_btn.configure(state="disabled")
        self.send_btn.configure(state="disabled")
        return True

    def start_voice(self):
        if self._ready_to_ask():
            threading.Thread(target=self._voice_worker, daemon=True).start()

    def send_text(self):
        text = self.entry.get().strip()
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
                elif time.time() - start > 5:
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
                self.events.put(("message", ("ai", f"Microphone problem: {e}")))
                return
            self.events.put(("level", 0))
            if not wav:
                self.events.put(("message", ("ai", "I didn't hear anything. Try again a bit louder.")))
                return
            self.events.put(("status", ("Thinking", AMBER)))
            text = Groq(api_key=self.cfg["api_key"]).audio.transcriptions.create(
                file=("q.wav", wav), model=STT_MODEL).text.strip()
            if not text:
                self.events.put(("message", ("ai", "Sorry, I couldn't understand that.")))
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

    def _answer(self, question):
        self.events.put(("status", ("Thinking", AMBER)))
        room = ""
        if self.sensor:
            room = (f" A sensor in the room currently reads {self.sensor[0]:.1f} C and "
                    f"{self.sensor[1]:.0f}% humidity; use it when asked about the room.")
        system = (f"You are {self.cfg['assistant_name']}, a friendly voice assistant inside a small "
                  "Arduino gadget with a 16x2 LCD. Reply in the user's language, in 1-3 short "
                  "sentences, plain text, no emojis or markdown." + room)
        self.history.append({"role": "user", "content": question})
        reply = Groq(api_key=self.cfg["api_key"]).chat.completions.create(
            model=self.cfg["model"],
            messages=[{"role": "system", "content": system}] + self.history[-10:],
            max_tokens=160,
        ).choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": reply})
        self.events.put(("message", ("ai", reply)))
        if self.arduino:
            self.arduino.send("A:" + reply)
        if self.cfg["speak"]:
            self.events.put(("status", ("Speaking", ACCENT)))
            speak(reply, self.cfg["voice_rate"])

    @staticmethod
    def _friendly_error(e):
        msg = str(e)
        if "401" in msg or "invalid_api_key" in msg.lower():
            return "Your API key doesn't work. Check it in ⚙ Settings."
        if "connect" in msg.lower() or "timeout" in msg.lower():
            return "I can't reach the internet right now. Check your connection."
        if "429" in msg:
            return "Too many requests - wait a few seconds and try again."
        return f"Something went wrong: {msg[:200]}"

    def on_close(self):
        if self.arduino:
            self.arduino.close()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
