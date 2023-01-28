#include <SoftwareSerial.h>

SoftwareSerial xbeeSerial(2,3); //Rx, Tx

void setup(){
  Serial.begin(9600);
  xbeeSerial.begin(9600);
}

void loop(){
if (xbeeSerial.available()) {
  int incomingByte = xbeeSerial.read();
  Serial.write(incomingByte);
}
}