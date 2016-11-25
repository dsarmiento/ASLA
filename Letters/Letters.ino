#include "SparkFunLSM6DS3.h"
#include "Wire.h"

#define M_PI 3.14159265359
#define GAIN 0.985
#define SENSORRATE  20

// Pin defines
#define greenLED    13
#define redLED       7
#define yellowLED    6

#define frontContact 5
#define sideContact  4

#define bigFinger A3
#define indexFinger A2
#define middleFinger A1
#define ringFinger  A0
#define pinkyFinger

bool testing = false;
LSM6DS3 handIMU(I2C_MODE, 0x6A);
long timer = 0;
float pitch = 0, pitchBase = 0;
float roll = 0, rollBase = 0;
float yaw = 0, yawBase = 0;
float accelX, accelY, accelZ, gyroX, gyroY, gyroZ;
float accelPitch, accelRoll, accelYaw;

void setup()
{
    pinMode(greenLED, OUTPUT);
    pinMode(redLED, OUTPUT);
    pinMode(yellowLED, OUTPUT);
    digitalWrite(greenLED, LOW);
    digitalWrite(yellowLED, LOW);
    digitalWrite(redLED, LOW);
    pinMode(frontContact, INPUT);
    pinMode(sideContact, INPUT);
    Serial.begin(115200);

    // Start handIMU
    if (handIMU.begin() != 0)
    {
        Serial.println("Problem starting sensor");
        digitalWrite(redLED, HIGH);
    }
    delay(1000);

    calibrate();
    timer = millis();
}


void loop()
{
    if(timer + SENSORRATE < millis())
    {
        timer = millis();
        readValues();
        pitch = GAIN * (pitch + gyroX * 0.01) + (1 - GAIN) * accelPitch;
        roll  = GAIN * (roll  + gyroY * 0.01) + (1 - GAIN) * accelRoll;
        yaw   = GAIN * (yaw   + gyroZ * 0.01) + (1 - GAIN) * accelYaw;
    }
    if(Serial.available() > 0 && Serial.read() == 'y')
    {
        String data = "";
        data += String(analogRead(0)); data += ",";
        data += String(analogRead(1)); data += ",";
        data += String(analogRead(2)); data += ",";
        data += String(analogRead(3)); data += ",";
        data += String(analogRead(6)); data += ",";
        data += String(digitalRead(frontContact) * 1023); data += ",";
        data += String(digitalRead(sideContact) * 1023); data += ",";
        data += String(yaw - yawBase); data += ",";
        data += String(pitch - pitchBase);
        Serial.println(data);
    }
}

void calibrate()
{
    digitalWrite(yellowLED, HIGH);
    for(int i = 0; i < 256; i++)
    {
        readValues();
        pitchBase = GAIN * (pitchBase + gyroX * 0.01) + (1 - GAIN) * accelPitch;
        rollBase  = GAIN * (rollBase  + gyroY * 0.01) + (1 - GAIN) * accelRoll;
        yawBase   = GAIN * (yawBase   + gyroZ * 0.01) + (1 - GAIN) * accelYaw;
        delay(10);
    }
    digitalWrite(yellowLED, LOW);
    digitalWrite(greenLED, HIGH);
}

void readValues()
{
    accelX = handIMU.readFloatAccelX();
    accelY = handIMU.readFloatAccelY();
    accelZ = handIMU.readFloatAccelZ();
    gyroX  = handIMU.readFloatGyroX();
    gyroY  = handIMU.readFloatGyroY();
    gyroZ  = handIMU.readFloatGyroZ();
    
    accelPitch = atan2(accelZ, accelY) * 180 / M_PI;
    accelRoll  = atan2(accelZ, accelX) * 180 / M_PI;
    accelYaw   = atan2(accelY, accelX) * 180 / M_PI;
}

