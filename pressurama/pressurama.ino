// From the datasheet:  https://www.nxp.com/docs/en/data-sheet/MPX4250D.pdf
// Vout = VCC × (P × 0.00369 + 0.04)
// P = pressure in kPa

int aiPins[] = {0,1,2,3,4,5,6,7};
int pinCount = 8;
unsigned long timer = 0;
long loopTime = 5000;   // microseconds

void setup() {
  Serial.begin(38400);
}

int number_of_measurements = 100;
float sum = 0;
float Vout = 0;
const float Vcc = 5.0;
float P = 0;

void loop() {
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    sum = 0;
    for (int i = 0; i < number_of_measurements; i++) {
      sum = sum + analogRead(aiPins[thisPin]);
    }
    Vout = 5.0 * (sum/number_of_measurements) / 1024.0;
    P = ((Vout/Vcc) - 0.04) / 0.00369;
    Serial.print(P);
    Serial.print("\t");
  }
  Serial.println();

    timeSync(loopTime);
  //int val = analogRead(0) - 512;
  double val = (analogRead(0) -512) / 512.0;
  sendToPC(&val);
}

void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000)
  {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0)
  {
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}

void sendToPC(int* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 2);
}

void sendToPC(double* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
