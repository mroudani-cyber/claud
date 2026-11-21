// AI Assistant for Arduino Uno + 16x2 I2C LCD + DHT11 + sound sensor
//
// Wiring:
//   LCD    : GND->GND, VCC->5V, SDA->A4, SCL->A5   (LED jumper must be on!)
//   DHT11  : VCC->5V, GND->GND, DATA->D2
//   Sound sensor (KY-037/KY-038/MAX4466): VCC->5V, GND->GND, AO->A0
//
// Arduino -> PC (115200 baud):
//   T:<temp>,<hum>   every 3 s
//   C                clap/loud sound detected (wake word)
// PC -> Arduino:
//   S:<text>   status (LISTENING / THINKING / ...) with animation
//   A:<text>   answer, scrolls on line 2
//   I          idle (face + temperature)

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define MIC_PIN A0
#define CLAP_THRESHOLD 120     // raise if it triggers too easily, lower if never

LiquidCrystal_I2C lcd(0x27, 16, 2);   // 0x3F if your scanner said so
DHT dht(DHTPIN, DHT11);

byte eyeOpen[8]   = {0b00000,0b01110,0b11111,0b11011,0b11011,0b11111,0b01110,0b00000};
byte eyeClosed[8] = {0b00000,0b00000,0b00000,0b11111,0b11111,0b00000,0b00000,0b00000};
byte thermo[8]    = {0b00100,0b01010,0b01010,0b01110,0b01110,0b11111,0b11111,0b01110};
byte drop[8]      = {0b00100,0b00100,0b01010,0b01010,0b10001,0b10001,0b10001,0b01110};
byte mic[8]       = {0b01110,0b01110,0b01110,0b01110,0b11111,0b01110,0b00100,0b01110};
byte dot[8]       = {0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b01100,0b01100};
byte waveLo[8]    = {0b00000,0b00000,0b00000,0b00100,0b00100,0b00000,0b00000,0b00000};
byte waveHi[8]    = {0b00000,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00000};

enum Mode { IDLE, STATUS, ANSWER };
Mode mode = IDLE;

String statusText, answer, inBuf;
int scrollPos = 0;
int frame = 0;
float temp = NAN, hum = NAN;
unsigned long lastTick = 0, lastDht = 0, lastClap = 0;

void drawIdle() {
  bool blink = (frame % 10 == 0);
  lcd.setCursor(0, 0);
  lcd.print("     ");
  lcd.write(blink ? 1 : 0);
  lcd.print("    ");
  lcd.write(blink ? 1 : 0);
  lcd.print("     ");
  lcd.setCursor(0, 1);
  if (isnan(temp)) {
    lcd.print(" clap to talk!  ");
  } else {
    lcd.write(2); lcd.print(temp, 0); lcd.print((char)223); lcd.print("C ");
    lcd.write(3); lcd.print(hum, 0); lcd.print("%  ");
    lcd.print((frame / 8) % 2 ? "clap" : "    ");
  }
}

void drawStatus() {
  lcd.setCursor(0, 0);
  lcd.write(4); lcd.print(" ");
  String s = statusText + "              ";
  lcd.print(s.substring(0, 14));
  lcd.setCursor(0, 1);
  bool listening = statusText.startsWith("LISTEN");
  for (int i = 0; i < 16; i++) {
    if (listening) lcd.write(((i * 7 + frame * 3) % 5) < 2 ? 7 : 6);
    else if (i % 2 == 0 && i / 2 < frame % 9) lcd.write(5);
    else lcd.print(" ");
  }
}

void drawAnswer() {
  lcd.setCursor(0, 0);
  lcd.print("AI:");
  lcd.write(frame % 2 ? 0 : 1);
  lcd.print("            ");
  int len = answer.length();
  lcd.setCursor(0, 1);
  for (int i = 0; i < 16; i++) {
    int idx = scrollPos + i - 16;          // starts off-screen to the right
    lcd.print((idx >= 0 && idx < len) ? answer[idx] : ' ');
  }
  if (++scrollPos > len + 16) scrollPos = 0;
}

void handleLine(String line) {
  line.trim();
  if (line.startsWith("S:"))      { statusText = line.substring(2); mode = STATUS; }
  else if (line.startsWith("A:")) { answer = line.substring(2); scrollPos = 0; mode = ANSWER; }
  else if (line == "I")           { mode = IDLE; }
  lcd.clear();
}

void checkClap() {
  // measure loudness over ~10 ms
  int lo = 1023, hi = 0;
  unsigned long t = millis();
  while (millis() - t < 10) {
    int v = analogRead(MIC_PIN);
    if (v < lo) lo = v;
    if (v > hi) hi = v;
  }
  if (hi - lo > CLAP_THRESHOLD && millis() - lastClap > 1500 && mode != STATUS) {
    lastClap = millis();
    Serial.println("C");
  }
}

void setup() {
  Serial.begin(115200);
  answer.reserve(200);
  inBuf.reserve(210);
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, eyeOpen);  lcd.createChar(1, eyeClosed);
  lcd.createChar(2, thermo);   lcd.createChar(3, drop);
  lcd.createChar(4, mic);      lcd.createChar(5, dot);
  lcd.createChar(6, waveLo);   lcd.createChar(7, waveHi);
  dht.begin();
  lcd.print("  AI Assistant");
  lcd.setCursor(0, 1); lcd.print("   starting...");
  delay(2000);
  lcd.clear();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { handleLine(inBuf); inBuf = ""; }
    else if (c != '\r' && inBuf.length() < 200) inBuf += c;
  }

  checkClap();

  if (millis() - lastDht > 3000) {
    lastDht = millis();
    float t = dht.readTemperature(), h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)) {
      temp = t; hum = h;
      Serial.print("T:"); Serial.print(t, 1); Serial.print(","); Serial.println(h, 0);
    }
  }

  if (millis() - lastTick >= (mode == ANSWER ? 300UL : 200UL)) {
    lastTick = millis();
    frame++;
    if (mode == IDLE) drawIdle();
    else if (mode == STATUS) drawStatus();
    else drawAnswer();
  }
}
