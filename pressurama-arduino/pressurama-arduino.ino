const byte numChars = 32;
char receivedChars[numChars];  // an array to store the received data
boolean newData = false;
long averages = 5;  // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
boolean programmed = false;

void setup() {
  Serial.begin(2000000);
  // while (!programmed) {
  //   recvWithEndMarker();
  //   showNewNumber();
  // }
}

void loop() {
  float sums[] = { 0, 0, 0, 0, 0, 0, 0, 0 };
  for (int measurement = 0; measurement < averages; measurement++) {
    for (int pin = 0; pin < 8; pin++) {
      sums[pin] += analogRead(pin);
    }
  }
  Serial.print("X ");
  for (int pin = 0; pin < 8; pin++) {
    Serial.print(pin);
    Serial.print(":");
    Serial.print(sums[pin] / averages);
    Serial.print(" ");
  }
  Serial.print("Y\n");
}



void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  if (Serial.available() > 0) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0';  // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}

void showNewNumber() {
  if (newData == true) {
    averages = 0;                    // new for this version
    averages = atol(receivedChars);  // new for this version
    Serial.print("This just in ... ");
    Serial.println(receivedChars);
    Serial.print("Data as Number ... ");  // new for this version
    Serial.println(averages);             // new for this version
    newData = false;
    programmed = true;
  }
}