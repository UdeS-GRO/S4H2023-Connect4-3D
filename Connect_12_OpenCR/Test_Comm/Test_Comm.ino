String nom = "Arduino";
String msg;
void setup() {
 	Serial.begin(9600);
}
void loop() {
 	readSerialPort();
 	if (msg != "") {
 			sendData();
 	}
 	delay(500);
}
str readSerialPort() {
 	msg = "";
 	if (Serial.available()) {
 			delay(10);
 			while (Serial.available() > 0) {
 					msg += (char)Serial.read();
 			}
 			Serial.flush();
 	}
  return msg;
}
void sendData() {
 	//write data
 	Serial.print(nom);
 	Serial.print(" received : ");
 	Serial.print(msg);
  Serial.println(600);
}