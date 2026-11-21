// AI Assistant display for Arduino Uno + 16x2 I2C LCD
// Wiring: GND->GND, VCC->5V, SDA->A4, SCL->A5
// Receives lines over USB serial (115200 baud) from assistant.py:
//   S:<text>   status mode (LISTENING / THINKING / SPEAKING ...) with animation
//   A:<text>   answer text, scrolls on line 2
//   I          idle face

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);   // change to 0x3F if your scanner said so

// ---- Custom characters ("textures") ----
byte eyeOpen[8]   = {0b00000,0b01110,0b11111,0b11011,0b11011,0b11111,0b01110,0b00000};
byte eyeClosed[8] = {0b00000,0b00000,0b00000,0b11111,0b11111,0b00000,0b00000,0b00000};
byte mouthL[8]    = {0b00000,0b00000,0b00000,0b10000,0b11000,0b01111,0b00111,0b00000};
byte mouthR[8]    = {0b00000,0b00000,0b00000,0b00001,0b00011,0b11110,0b11100,0b00000};
byte mic[8]       = {0b01110,0b01110,0b01110,0b01110,0b11111,0b01110,0b00100,0b01110};
byte dot1[8]      = {0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b01100,0b01100};
byte wave1[8]     = {0b00000,0b00000,0b00000,0b00100,0b00100,0b00000,0b00000,0b00000};
byte wave2[8]     = {0b00000,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00000};

enum Mode { IDLE, STATUS, ANSWER };
Mode mode = IDLE;

String statusText = "";
String answer = "";
String inBuf = "";
int scrollPos = 0;
unsigned long lastTick = 0;
int frame = 0;

void clearLine(int row) {
  lcd.setCursor(0, row);
  lcd.print("                ");
  lcd.setCursor(0, row);
}

void drawIdle() {
  lcd.clear();
  bool blink = (frame % 8 == 0);
  lcd.setCursor(5, 0); lcd.write(blink ? 1 : 0);
  lcd.setCursor(10, 0); lcd.write(blink ? 1 : 0);
  lcd.setCursor(6, 1); lcd.write(2);
  lcd.print("  ");
  lcd.write(3);
}

void drawStatus() {
  clearLine(0);
  lcd.write(4);                 // mic icon
  lcd.print(" ");
  lcd.print(statusText.substring(0, 14));
  clearLine(1);
  // animated bars / dots
  for (int i = 0; i < 16; i++) {
    int h = (i + frame) % 4;
    if (statusText.startsWith("LISTEN")) lcd.write(h < 2 ? 6 : 7);
    else if (i < (frame % 4) * 2 + 2 && i % 2 == 0) lcd.write(5);
    else lcd.print(" ");
  }
}

void drawAnswer() {
  // line 1: header, line 2: scrolling text
  lcd.setCursor(0, 0);
  lcd.print("AI:             ");
  String padded = "                " + answer + "                ";
  int maxPos = padded.length() - 16;
  if (scrollPos > maxPos) scrollPos = 0;
  lcd.setCursor(0, 1);
  lcd.print(padded.substring(scrollPos, scrollPos + 16));
  scrollPos++;
}

void handleLine(String line) {
  line.trim();
  if (line.startsWith("S:")) {
    statusText = line.substring(2); mode = STATUS; lcd.clear();
  } else if (line.startsWith("A:")) {
    answer = line.substring(2); scrollPos = 0; mode = ANSWER; lcd.clear();
  } else if (line == "I") {
    mode = IDLE;
  }
}

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, eyeOpen);
  lcd.createChar(1, eyeClosed);
  lcd.createChar(2, mouthL);
  lcd.createChar(3, mouthR);
  lcd.createChar(4, mic);
  lcd.createChar(5, dot1);
  lcd.createChar(6, wave1);
  lcd.createChar(7, wave2);
  lcd.setCursor(0, 0); lcd.print("  AI Assistant");
  lcd.setCursor(0, 1); lcd.print("   starting...");
  delay(1500);
  drawIdle();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { handleLine(inBuf); inBuf = ""; }
    else if (inBuf.length() < 300) inBuf += c;
  }

  unsigned long speed = (mode == ANSWER) ? 300 : 250;
  if (millis() - lastTick >= speed) {
    lastTick = millis();
    frame++;
    if (mode == IDLE) drawIdle();
    else if (mode == STATUS) drawStatus();
    else drawAnswer();
  }
}
