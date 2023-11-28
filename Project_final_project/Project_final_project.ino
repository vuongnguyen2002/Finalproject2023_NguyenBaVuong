#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
Servo myservo;
LiquidCrystal_I2C lcd(0x27, 16, 2);
int x_pin = A0;
int y_pin = A1;
int pos = 0;
const int IR_PIN = 13;
const int buzzer = 7;
const int led = 9;
int val;
const int tri_pin = 8;
const int ech_pin = 6;
long duration;
int distance;
int servoVal;

int option;
void setup() {
  // initialize the LCD
  lcd.begin();

  // Turn on the blacklight and print a message.
  lcd.backlight();

  // Turn on the blacklight and print a message.
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(IR_PIN, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(led, OUTPUT);
  myservo.attach(10);
  pinMode(tri_pin, OUTPUT);
  pinMode(ech_pin, INPUT);
  myservo.write(pos);
}

void loop() {

  // ultrasonic
  digitalWrite(tri_pin, LOW);
  delayMicroseconds(2);

  digitalWrite(tri_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(tri_pin, LOW);

  duration = pulseIn(ech_pin, HIGH);
  distance = (duration / 2) * 0.0344;


  if (distance >= 10 || distance <= 2) {
    lcd.setCursor(1, 0);
    lcd.println(" No detect :))) ");
    delay(2000);
    lcd.clear();

  } else {
    lcd.setCursor(0, 0);
    lcd.print("Detective: ");
    lcd.print(distance);
    lcd.print(" cm ");
    delay(100);
  }
  // motor vervo
  for (pos = 0; pos <= 180; pos += 1) {
    myservo.write(pos);
    delay(10);
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(10);
  }
  
  val = digitalRead(IR_PIN);
  Serial.print("Motion detected ");
  Serial.println(val);
  Serial.println(" ");

  if (val == 0) {
    myservo.write(140);
    tone(buzzer, 500);
    digitalWrite(led, HIGH);
    delay(2000);
    Serial.println("----------- ALARM ACTIVATED -----------");
    
  } else {
    myservo.write(0);
    noTone(buzzer);
    digitalWrite(led, LOW);

    Serial.println("ALARM DEACTIVATED");
  }
}
