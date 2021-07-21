// From the datasheet:  https://www.nxp.com/docs/en/data-sheet/MPX4250D.pdf
// Vout = VCC × (P × 0.00369 + 0.04)
// P = pressure in kPa

int aiPins[] = {0};
int pinCount = 8;

void setup() {
  Serial.begin(2000000);
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
}
