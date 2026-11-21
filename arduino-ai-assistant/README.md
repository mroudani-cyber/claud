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
