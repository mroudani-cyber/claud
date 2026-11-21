// AI Assistant for Arduino Uno + 16x2 I2C LCD + DHT11 + KY-037 sound sensor + buzzer
//
// Wiring:
//   LCD    : GND->GND, VCC->5V, SDA->A4, SCL->A5   (LED jumper must be on!)
//   DHT11  : VCC->5V, GND->GND, DATA->D2
//   KY-037 : +->5V, G->GND, AO->A0, DO->D3 (DO is optional but makes claps more reliable)
//   Buzzer : one leg -> D13, other leg -> GND
//
// Arduino -> PC (115200 baud):
//   T:<temp>,<hum>        every 3 s
//   C                     clap detected
//   L:<level>,<avg>,<do>  live sound level (only while the app's sensor test is on)
// PC -> Arduino:
//   S:<text>   status (LISTENING / THINKING ...)    A:<text>  answer (scrolls)
//   I          idle face                             P:<name>  play hello/alert/test
//   B:<0|1|2>  buzzer off / beeps / beeps + robot voice
//   K:<n>      clap sensitivity (lower = more sensitive, default 20)
//   M:<0|1>    live sound level for the sensor test

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define MIC_PIN A0
#define MIC_DO_PIN 3
#define BUZZER_PIN 13

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
unsigned long lastTick = 0, lastDht = 0, lastClap = 0, lastLevel = 0;

// ---------- sound sensor
int clapSens = 20;          // how far above the background noise a clap must be
float noiseAvg = 5;         // running average of the background noise
int doIdle = HIGH;          // resting state of the DO pin
bool monitor = false;

// ---------- buzzer
struct Note { int f; int d; };          // f = 0 means silence, {0,0} ends a sound
const Note SND_HELLO[]  = {{523,90},{659,90},{784,90},{1047,160},{0,0}};
const Note SND_LISTEN[] = {{880,60},{1319,90},{0,0}};
const Note SND_THINK[]  = {{700,35},{0,70},{900,35},{0,0}};
const Note SND_DONE[]   = {{1047,70},{0,30},{1568,110},{0,0}};
const Note SND_ALERT[]  = {{1800,140},{0,90},{1800,140},{0,90},{1800,140},{0,0}};
const Note* melody = NULL;
int noteIdx = 0;
unsigned long noteEnd = 0, talkUntil = 0, nextChirp = 0, quietUntil = 0;
byte buzzMode = 2;          // 0 off, 1 beeps, 2 beeps + robot voice

void play(const Note* m) {
  if (buzzMode == 0) return;
  melody = m; noteIdx = -1; noteEnd = 0;
}

void updateSound() {
  unsigned long now = millis();
  if (melody) {
    if (now >= noteEnd) {
      noteIdx++;
      Note n = melody[noteIdx];
      if (n.f == 0 && n.d == 0) { melody = NULL; noTone(BUZZER_PIN); return; }
      if (n.f) tone(BUZZER_PIN, n.f, n.d); else noTone(BUZZER_PIN);
      noteEnd = now + n.d + 10;
    }
    quietUntil = now + 350;           // don't hear our own beeps as a clap
    return;
  }
  if (buzzMode == 2 && now < talkUntil && now >= nextChirp) {   // R2-style "talking"
    int d = random(35, 85);
    tone(BUZZER_PIN, random(600, 2000), d);
    nextChirp = now + d + random(25, 110);
    quietUntil = now + 350;
  }
}

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
  if (line.length() == 0) return;
  if (line.startsWith("S:")) {
    statusText = line.substring(2); mode = STATUS; lcd.clear();
    talkUntil = 0;
    if (statusText.startsWith("LISTEN")) play(SND_LISTEN);
    else if (statusText.startsWith("THINK")) play(SND_THINK);
  } else if (line.startsWith("A:")) {
    answer = line.substring(2); scrollPos = 0; mode = ANSWER; lcd.clear();
    play(SND_DONE);
    talkUntil = millis() + 250 + min((unsigned long)answer.length() * 45UL, 5000UL);
  } else if (line == "I") {
    mode = IDLE; talkUntil = 0; lcd.clear();
  } else if (line.startsWith("B:")) {
    buzzMode = constrain(line.substring(2).toInt(), 0, 2);
    melody = NULL; talkUntil = 0; noTone(BUZZER_PIN);
  } else if (line.startsWith("P:")) {
    String n = line.substring(2);
    if (n == "alert") play(SND_ALERT);
    else if (n == "listen") play(SND_LISTEN);
    else if (n == "test") { play(SND_HELLO); if (buzzMode == 2) talkUntil = millis() + 1800; }
    else play(SND_HELLO);
  } else if (line.startsWith("K:")) {
    clapSens = constrain(line.substring(2).toInt(), 3, 300);
  } else if (line.startsWith("M:")) {
    monitor = line.substring(2) == "1";
  }
}

void checkClap() {
  // loudness = peak-to-peak of the analog signal over ~8 ms
  int lo = 1023, hi = 0;
  bool doHit = false;
  unsigned long t = millis();
  while (millis() - t < 8) {
    int v = analogRead(MIC_PIN);
    if (v < lo) lo = v;
    if (v > hi) hi = v;
    if (digitalRead(MIC_DO_PIN) != doIdle) doHit = true;
  }
  int level = hi - lo;
  unsigned long now = millis();

  if (monitor && now - lastLevel > 100) {
    lastLevel = now;
    Serial.print("L:"); Serial.print(level); Serial.print(",");
    Serial.print((int)noiseAvg); Serial.print(","); Serial.println(doHit ? 1 : 0);
  }

  bool quiet = now < quietUntil || melody != NULL;
  bool spike = level > noiseAvg * 2 + clapSens;
  if (!spike) noiseAvg = noiseAvg * 0.98 + level * 0.02;   // learn the background noise

  if (!quiet && (spike || doHit) && now - lastClap > 1500 && mode != STATUS) {
    lastClap = now;
    Serial.println("C");
  }
}

void setup() {
  Serial.begin(115200);
  answer.reserve(200);
  inBuf.reserve(210);
  pinMode(MIC_DO_PIN, INPUT_PULLUP);
  randomSeed(analogRead(A1));
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, eyeOpen);  lcd.createChar(1, eyeClosed);
  lcd.createChar(2, thermo);   lcd.createChar(3, drop);
  lcd.createChar(4, mic);      lcd.createChar(5, dot);
  lcd.createChar(6, waveLo);   lcd.createChar(7, waveHi);
  dht.begin();
  lcd.print("  AI Assistant");
  lcd.setCursor(0, 1); lcd.print("   starting...");
  play(SND_HELLO);

  // learn the resting state of DO and the background noise (keep quiet for 1.5 s)
  int highs = 0, n = 0;
  long sum = 0;
  unsigned long t0 = millis();
  while (millis() - t0 < 1500) {
    updateSound();
    if (digitalRead(MIC_DO_PIN) == HIGH) highs++;
    int lo = 1023, hi = 0;
    for (int i = 0; i < 40; i++) { int v = analogRead(MIC_PIN); lo = min(lo, v); hi = max(hi, v); }
    if (millis() - t0 > 600) { sum += hi - lo; n++; }
  }
  doIdle = highs > 50 ? HIGH : LOW;
  if (n) noiseAvg = max(2L, sum / n);
  lcd.clear();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { handleLine(inBuf); inBuf = ""; }
    else if (c != '\r' && inBuf.length() < 200) inBuf += c;
  }

  updateSound();
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
