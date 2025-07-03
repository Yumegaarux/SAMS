#include <LiquidCrystal_I2C.h>
#include <ThreeWire.h>
#include <RtcDS1302.h>
#include <Servo.h>

// LCD & RTC Setup
LiquidCrystal_I2C lcd(0x27, 16, 2);
ThreeWire myWire(7, 6, 8);
RtcDS1302<ThreeWire> Rtc(myWire);

// Servo Setup
Servo servo1, servo2;
const int servoPin1 = 10;
const int servoPin2 = 9;

// Flags and Pins
bool servoActivated = false;
bool servoWebActivated = false;
int btnPin = 5;
int ledPin = 3;

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();

  pinMode(btnPin, INPUT);
  pinMode(ledPin, OUTPUT);

  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo1.write(10);
  servo2.write(160);

  Serial.begin(9600);

  Rtc.Begin();

  // Uncomment this if you want to set RTC manually:
  //RtcDateTime currentTime = RtcDateTime(__DATE__, __TIME__);
  //Rtc.SetDateTime(currentTime);
}

void loop() {
  RtcDateTime now = Rtc.GetDateTime();
  lcd.clear();

  // Display Date
  lcd.setCursor(0, 0);
  lcd.print("Date: ");
  lcd.print(now.Day());
  lcd.print("/");
  lcd.print(now.Month());
  lcd.print("/");
  lcd.print(now.Year());

  // Display Time
  lcd.setCursor(0, 1);
  lcd.print("Time: ");
  lcd.print(now.Hour());
  lcd.print(":");
  lcd.print(now.Minute());
  lcd.print(":");
  lcd.print(now.Second());

  // Scheduled Activation
  if ((now.Hour() == 0 && now.Minute() == 11 && now.Second() == 0 && !servoActivated) ||
      (now.Hour() == 12 && now.Minute() == 30 && now.Second() == 0 && !servoActivated) ||
      (now.Hour() == 18 && now.Minute() == 30 && now.Second() == 0 && !servoActivated)) {
    activateServos();
    servoActivated = true;
  }

  // Reset servoActivated flag when second is not 0
  if (now.Second() != 0) {
    servoActivated = false;
  }

  // Manual Activation via Button
  if (digitalRead(btnPin) == HIGH) {
    activateServos();
  }

  // Serial Command from ESP32
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "servo" && !servoWebActivated) {
      webactivateServos();
      servoWebActivated = true;
    }
  }

  // Reset the webActivated flag to allow new triggers on new commands
  // (Optional: adjust timing or logic if needed)
  if (!Serial.available()) {
    servoWebActivated = false;
  }

  delay(1000);
}

void activateServos() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Food Dispensing");

  servo1.write(80);  // Rotate Servo 1
  servo2.write(90);  // Rotate Servo 2
  digitalWrite(ledPin, HIGH);
  delay(1500);

  servo1.write(10);  // Reset Servo 1
  servo2.write(160); // Reset Servo 2
  digitalWrite(ledPin, LOW);

  // Refresh display
  RtcDateTime now = Rtc.GetDateTime();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Date: ");
  lcd.print(now.Day());
  lcd.print("/");
  lcd.print(now.Month());
  lcd.print("/");
  lcd.print(now.Year());

  lcd.setCursor(0, 1);
  lcd.print("Time: ");
  lcd.print(now.Hour());
  lcd.print(":");
  lcd.print(now.Minute());
  lcd.print(":");
  lcd.print(now.Second());
}

void webactivateServos() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Food Dispensing");

  servo1.write(80);  // Rotate Servo 1
  servo2.write(90);  // Rotate Servo 2
  digitalWrite(ledPin, HIGH);
  delay(2500);

  servo1.write(10);  // Reset Servo 1
  servo2.write(160); // Reset Servo 2
  digitalWrite(ledPin, LOW);

  // Refresh display
  RtcDateTime now = Rtc.GetDateTime();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Date: ");
  lcd.print(now.Day());
  lcd.print("/");
  lcd.print(now.Month());
  lcd.print("/");
  lcd.print(now.Year());

  lcd.setCursor(0, 1);
  lcd.print("Time: ");
  lcd.print(now.Hour());
  lcd.print(":");
  lcd.print(now.Minute());
  lcd.print(":");
  lcd.print(now.Second());
}
