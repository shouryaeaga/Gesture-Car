#include <Arduino.h>
#include "Wifi.h"

void setup() {
// write your initialization code here
    Serial.begin(115200); // Initialize serial communication at 115200 baud rate
    Serial.println("Hello, world!");
}

void loop() {
// write your code here
    Serial.println("Hello, world!");
    delay(1000); // Delay for 1 second
}