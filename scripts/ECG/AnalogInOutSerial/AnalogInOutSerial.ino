
const int analogInPin = A1;  // Analog input pin that the potentiometer is attached to


int sensorValue = 0;        // value read from the pot


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);

  // print the results to the serial monitor:
  Serial.println(sensorValue);
  // wait 2 milliseconds before the next loop
  delay(5);
}
