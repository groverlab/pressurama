// From the datasheet:  https://www.nxp.com/docs/en/data-sheet/MPX4250D.pdf
// Vout = VCC × (P × 0.00369 + 0.04)
// P = pressure in kPa
int vals[9];
int aiPins[] = {0,1,2,3,4,5,6,7,8,9};
int pinCount = 10;

void setup() {
  Serial.begin(9600);
}

int number_of_measurements = 10;
float sum = 0;
float Vout = 0;
const float Vcc = 5.0;


void loop() {
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    sum = 0;
    for (int i = 0; i < number_of_measurements; i++) {
      sum = sum + analogRead(aiPins[thisPin]);
      Vout = 5.0 * (sum/number_of_measurements) / 1024.0;
      vals[thisPin] = 100 *((Vout/Vcc) - 0.04) / 0.00369;
    }
    Serial.println(vals[thisPin]);
  }
  delay(1100)
}
