void setup() {
  Serial.begin(2000000);
}

void loop() {
  Serial.print("X ");
  for(int pin = 0; pin < 8; pin++) {
    Serial.print(pin);
    Serial.print(":");
    Serial.print(analogRead(pin));
    Serial.print(" ");
  }
  Serial.print("Y\n");
//  delay(1000);
}
