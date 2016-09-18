#include "SparkFunLSM6DS3.h"
#include "Wire.h"
#include "SPI.h"

LSM6DS3 SensorOne( I2C_MODE, 0x6A );
LSM6DS3 SensorTwo( I2C_MODE, 0x6B );
bool testing = false;

void setup()
{
    Serial.begin(57600);
    delay(1000);
    if(SensorOne.begin() != 0)
    {
        Serial.println("Problem starting sensor 0x6A");
    }
    if(SensorTwo.begin() != 0)
    {
        Serial.println("Problem starting sensor 0x6B");
    }
}

void loop()
{
    
    long start = millis();
    int cnt = 0;
    while(start + 1000 > millis()){
      String data = "";
    data += String(analogRead(0)); data += ",";
    data += String(analogRead(1)); data += ",";
    data += String(analogRead(2)); data += ",";
    data += String(analogRead(3)); data += ",";
    data += String(SensorOne.readFloatAccelX()); data += ",";
    data += String(SensorOne.readFloatAccelY()); data += ",";
    data += String(SensorOne.readFloatAccelZ()); data += ",";
    data += String(SensorOne.readFloatGyroX()); data += ",";
    data += String(SensorOne.readFloatGyroY()); data += ",";
    data += String(SensorOne.readFloatGyroZ()); data += ",";
    data += String(SensorTwo.readFloatAccelX()); data += ",";
    data += String(SensorTwo.readFloatAccelY()); data += ",";
    data += String(SensorTwo.readFloatAccelZ()); data += ",";
    data += String(SensorTwo.readFloatGyroX()); data += ",";
    data += String(SensorTwo.readFloatGyroY()); data += ",";
    data += String(SensorTwo.readFloatGyroZ());
    
    long end = millis();
    
    if(testing)
    {
        Serial.println(end-start);
    }
    else
    {
        Serial.println(data);
        cnt++;
    }
    }
    Serial.println(cnt);
    while(true);
}


