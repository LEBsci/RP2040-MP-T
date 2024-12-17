#include <WiFiNINA.h>
#include <Wire.h>
#include <Arduino_LSM6DSOX.h>
#include <SPI.h>
#include "arduino_secrets.h" 

const char* ssid = SECRET_SSID;
const char* pass = SECRET_PASS;

WiFiServer server(80);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);  // Initialize the LED_BUILTIN pin as an output

  Serial.begin(9600);
  while (!Serial);

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  int status = WL_IDLE_STATUS; // Initialize the status variable

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(10000);
  }
  
  Serial.println("Connected to WiFi");

  // Print the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1) {
      delay(10);
    }
  }
  Serial.println("IMU initialized!");

  server.begin();
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED on
  delay(2000);

  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == '\n') {
          if (currentLine.length() == 0) {
            int temperature;
            if (IMU.temperatureAvailable()) {
              IMU.readTemperature(temperature);
            }
            String temperatureStr = String(temperature);

            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/plain");
            client.println();
            client.println(temperatureStr);
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected.");
  }

  digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off

  delay(3000);  // Measure and post temperature every 5 seconds
}