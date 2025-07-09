#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "secrets.h" // Ensure this file contains your WiFi and MQTT credentials


WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

#define AMBER 25
#define GREEN 23

#define EN_TL 13
#define A1_TL_BACKWARDS 33
#define A2_TL_FORWARDS 27

#define EN_BL 14
#define A3_BL_BACKWARDS 26
#define A4_BL_FORWARDS 32

#define EN_BR 4
#define A3_BR_BACKWARDS 16
#define A4_BR_FORWARDS 17

#define EN_TR 18
#define A1_TR_BACKWARDS 21
#define A2_TR_FORWARDS 19

void callback(char* topic, byte* payload, unsigned int length);

void forwards();
void backwards();
void stopMotors();
void left();
void right();


void setup() {
  Serial.begin(115200);

  pinMode(AMBER, OUTPUT);
  pinMode(GREEN, OUTPUT);
  digitalWrite(AMBER, LOW);
  digitalWrite(GREEN, LOW);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Wifi Connected");
  Serial.println(WiFi.localIP());
  digitalWrite(AMBER, HIGH);
  digitalWrite(GREEN, LOW);

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  pinMode(EN_TL, OUTPUT);
  pinMode(A1_TL_BACKWARDS, OUTPUT);
  pinMode(A2_TL_FORWARDS, OUTPUT);

  pinMode(EN_BL, OUTPUT);
  pinMode(A3_BL_BACKWARDS, OUTPUT);
  pinMode(A4_BL_FORWARDS, OUTPUT);

  pinMode(EN_BR, OUTPUT);
  pinMode(A3_BR_BACKWARDS, OUTPUT);
  pinMode(A4_BR_FORWARDS, OUTPUT);

  pinMode(EN_TR, OUTPUT);
  pinMode(A1_TR_BACKWARDS, OUTPUT);
  pinMode(A2_TR_FORWARDS, OUTPUT);
}

void loop() {
  if (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Connected to MQTT");
      client.subscribe("gesture/direction");
      digitalWrite(GREEN, HIGH);
      digitalWrite(AMBER, LOW);
    } else {
      Serial.print("Failed to connect, state: ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Check payload by converting to string
  String command = String((char*)payload).substring(0, length);
  command.trim(); // Remove any leading/trailing whitespace

  if (command == "UP") {
    forwards();
  } else if (command == "DOWN") {
    backwards();
  } else if (command == "LEFT") {
    left();
  } else if (command == "RIGHT") {
    right();
  } else if (command == "STOP") {
    stopMotors();
  } else {
    Serial.println("Unknown command received");
    stopMotors(); // Stop motors if command is unknown
  }

  delay(10); // Small delay to ensure commands are processed
}

void forwards() {
  digitalWrite(EN_TL, HIGH);
  digitalWrite(A1_TL_BACKWARDS, LOW);
  digitalWrite(A2_TL_FORWARDS, HIGH);

  digitalWrite(EN_BL, HIGH);
  digitalWrite(A3_BL_BACKWARDS, LOW);
  digitalWrite(A4_BL_FORWARDS, HIGH);

  digitalWrite(EN_BR, HIGH);
  digitalWrite(A3_BR_BACKWARDS, LOW);
  digitalWrite(A4_BR_FORWARDS, HIGH);

  digitalWrite(EN_TR, HIGH);
  digitalWrite(A1_TR_BACKWARDS, LOW);
  digitalWrite(A2_TR_FORWARDS, HIGH);
}

void backwards() {
  digitalWrite(EN_TL, HIGH);
  digitalWrite(A1_TL_BACKWARDS, HIGH);
  digitalWrite(A2_TL_FORWARDS, LOW);

  digitalWrite(EN_BL, HIGH);
  digitalWrite(A3_BL_BACKWARDS, HIGH);
  digitalWrite(A4_BL_FORWARDS, LOW);

  digitalWrite(EN_BR, HIGH);
  digitalWrite(A3_BR_BACKWARDS, HIGH);
  digitalWrite(A4_BR_FORWARDS, LOW);

  digitalWrite(EN_TR, HIGH);
  digitalWrite(A1_TR_BACKWARDS, HIGH);
  digitalWrite(A2_TR_FORWARDS, LOW);
}

void stopMotors() {
  digitalWrite(EN_TL, LOW);
  digitalWrite(A1_TL_BACKWARDS, LOW);
  digitalWrite(A2_TL_FORWARDS, LOW);

  digitalWrite(EN_BL, LOW);
  digitalWrite(A3_BL_BACKWARDS, LOW);
  digitalWrite(A4_BL_FORWARDS, LOW);

  digitalWrite(EN_BR, LOW);
  digitalWrite(A3_BR_BACKWARDS, LOW);
  digitalWrite(A4_BR_FORWARDS, LOW);

  digitalWrite(EN_TR, LOW);
  digitalWrite(A1_TR_BACKWARDS, LOW);
  digitalWrite(A2_TR_FORWARDS, LOW);
}

void left() {
  // tank turning
  digitalWrite(EN_TL, HIGH);
  digitalWrite(A1_TL_BACKWARDS, HIGH);
  digitalWrite(A2_TL_FORWARDS, LOW);

  digitalWrite(EN_BL, HIGH);
  digitalWrite(A3_BL_BACKWARDS, HIGH);
  digitalWrite(A4_BL_FORWARDS, LOW);

  digitalWrite(EN_BR, HIGH);
  digitalWrite(A3_BR_BACKWARDS, LOW);
  digitalWrite(A4_BR_FORWARDS, HIGH);

  digitalWrite(EN_TR, HIGH);
  digitalWrite(A1_TR_BACKWARDS, LOW);
  digitalWrite(A2_TR_FORWARDS, HIGH);
}

void right() {
  // tank turning
  digitalWrite(EN_TL, HIGH);
  digitalWrite(A1_TL_BACKWARDS, LOW);
  digitalWrite(A2_TL_FORWARDS, HIGH);

  digitalWrite(EN_BL, HIGH);
  digitalWrite(A3_BL_BACKWARDS, LOW);
  digitalWrite(A4_BL_FORWARDS, HIGH);

  digitalWrite(EN_BR, HIGH);
  digitalWrite(A3_BR_BACKWARDS, HIGH);
  digitalWrite(A4_BR_FORWARDS, LOW);

  digitalWrite(EN_TR, HIGH);
  digitalWrite(A1_TR_BACKWARDS, HIGH);
  digitalWrite(A2_TR_FORWARDS, LOW);
}