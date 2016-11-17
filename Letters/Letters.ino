#include "SparkFunLSM6DS3.h"
#include "Wire.h"

#define M_PI 3.14159265359
#define GAIN 0.965

#define statusLED 13

bool testing = false;
LSM6DS3 IMU(I2C_MODE, 0x6B);
long timer = 0, printTimer = 0;
double pitch = 0, pitchBase = 0;
double roll = 0, rollBase = 0;
double yaw = 0, yawBase = 0;
double accelX, accelY, accelZ, gyroX, gyroY, gyroZ;
double accelPitch, accelRoll, accelYaw;

void setup()
{
    pinMode(statusLED, OUTPUT);
    pinMode(8, INPUT);
    pinMode(9, INPUT);
    Serial.begin(115200);
    if (IMU.begin() != 0)
    Serial.println("Problem starting sensor");
    delay(1000);

    digitalWrite(statusLED, HIGH);
    calibrate();
    digitalWrite(statusLED, LOW);
    Serial.println(String(pitchBase) + "\t" + String(rollBase));
    timer = millis();
}


void loop()
{
    if(timer + 20 < millis())
    {
        timer = millis();
        
        accelX = IMU.readFloatAccelX();
        accelY = IMU.readFloatAccelY();
        accelZ = IMU.readFloatAccelZ();
        gyroX = IMU.readFloatGyroX();
        gyroY = IMU.readFloatGyroY();
        gyroZ = IMU.readFloatGyroZ();
        
        accelPitch = atan2(accelZ, accelY) * 180 / M_PI;
        accelRoll  = atan2(accelZ, accelX) * 180 / M_PI;
        accelYaw  = atan2(accelY, accelX) * 180 / M_PI;
        pitch = GAIN * (pitch + gyroX * 0.01) + (1 - GAIN) * accelPitch;
        roll  = GAIN * (roll  + gyroY * 0.01) + (1 - GAIN) * accelRoll;
        yaw   = GAIN * (yaw   + gyroZ * 0.01) + (1 - GAIN) * accelYaw;
    }
    if(printTimer + 50 < millis())
    {
        printTimer = millis();
        
        String data = "";
        data += String(analogRead(0)); data += ",";
        data += String(analogRead(1)); data += ",";
        data += String(analogRead(2)); data += ",";
        data += String(analogRead(3)); data += ",";
        data += String(analogRead(6)); data += ",";
        data += String(digitalRead(8) * 1023); data += ",";
        data += String(digitalRead(9) * 1023); data += ",";
        data += String(yaw - yawBase); data += ",";
        data += String(pitch - pitchBase);
        Serial.println(data);
    }
}

void calibrate()
{
  for(int i = 0; i < 256; i++)
  {
    accelX = IMU.readFloatAccelX();
    accelY = IMU.readFloatAccelY();
    accelZ = IMU.readFloatAccelZ();
    gyroX = IMU.readFloatGyroX();
    gyroY = IMU.readFloatGyroY();
    gyroZ = IMU.readFloatGyroZ();
    
    accelPitch = atan2(accelZ, accelY) * 180 / M_PI;
    accelRoll  = atan2(accelZ, accelX) * 180 / M_PI;
        accelYaw  = atan2(accelY, accelX) * 180 / M_PI;
    pitchBase = GAIN * (pitchBase + gyroX * 0.01) + (1 - GAIN) * accelPitch;
    rollBase  = GAIN * (rollBase  + gyroY * 0.01) + (1 - GAIN) * accelRoll;
    yawBase   = GAIN * (yawBase   + gyroZ * 0.01) + (1 - GAIN) * accelYaw;
    delay(10);
  }

}


