# Arduino AI Assistant

The PC does the "brain" work (microphone, AI, speaker). The Arduino Uno shows
status animations and the answer on the 16x2 I2C LCD.

1. Arduino IDE: install library "LiquidCrystal I2C" (Frank de Brabander),
   upload `lcd_display/lcd_display.ino`. Close the Serial Monitor afterwards.
2. Get a free API key at https://console.groq.com
3. On the PC:
   ```
   pip install groq pyserial sounddevice numpy scipy pyttsx3 unidecode
   set GROQ_API_KEY=your_key_here
   python assistant.py --port COM5
   ```

## Windows app (.exe) - v2

In `app/`, double-click **BUILD_EXE.bat** (needs Python). It creates
`AI-Assistant.exe` in the same folder.

Features: chat + mic button, Ctrl+Space to talk, clap to talk, live room
temperature/humidity, hot-room alerts, quick buttons, personalities, languages,
Windows voices, dark/light theme, accent colours, text size, chat history and
export, send your own text to the LCD, and **auto-updates**.

Auto-updates: the exe checks `app/version.json` on GitHub at startup. When the
version there is higher, it downloads the new `ai_assistant_app.py` and uses it
after a restart (no need to rebuild the exe). Bump `version.json` and
`APP_VERSION` together when you publish a change. Updates that need new Python
packages still require rebuilding the exe.

Run without building: `python launcher.py`.
