bool testing = false;

void setup()
{
    Serial.begin(115200);
    delay(1000);
}

void loop()
{
  int start = millis();
  String data = "";
  data += String(analogRead(0)); data += ","; // Thumb
  data += String(analogRead(1)); data += ","; // Index
  data += String(analogRead(2)); data += ","; // Middle
  data += String(analogRead(3)); data += ","; // Ring
  data += String(analogRead(6)); data += ","; // Pinkey
  data += String(digitalRead(8)); data += ","; // Side
  data += String(digitalRead(9)); // Bottom
  int end = millis();  

  if(Serial.available() > 0)
  {
    char in = Serial.read();
    if(in == 'y')
    {
      if(testing)
      {
        Serial.println(end-start);
      }
      else
      {
        Serial.println(data);
      }
    }
  }
}


