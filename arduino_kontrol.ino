#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 150  // Minimum açı değeri (servo motorun minimum dönebileceği açı)
#define SERVO_MAX 600  // Maksimum açı değeri (servo motorun maksimum dönebileceği açı)

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();



void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  // PWM frekansını 60 Hz olarak ayarlayabilirsiniz
}

void loop() {
  if (Serial.available() > 0) {
    // Seri haberleşme ile Python'dan gelen verileri alıyoruz
    int servoNum = Serial.parseInt();  // Servo numarası
    char delimiter = Serial.read();    // Delimiter karakterini alıyoruz
    int angle = Serial.parseInt();     // Döndürmek istediğimiz açı değeri

    // Açı değerini sınırlıyoruz
    angle = constrain(angle, 0, 180);

    // Açı değerini PWM sinyaline çeviriyoruz
    int pwmValue = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);

    // Servo motoru döndürüyoruz
    pwm.setPWM(servoNum, 0, pwmValue);
  }
}
