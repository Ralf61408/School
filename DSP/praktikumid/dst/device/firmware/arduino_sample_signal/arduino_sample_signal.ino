int value = 0;

void setup() {
  Serial.begin(9600);
 

}

void loop() {
  value = analogRead(A0); // Loeme analoogsignaali väärtuse pordist A0
  Serial.println(value); // Saadame loetud väärtuse üle Serial ühenduse arvutisse
  delay(50); // Ootame 50 ms, et saavutada 20 Hz mõõtmise sagedus

}
