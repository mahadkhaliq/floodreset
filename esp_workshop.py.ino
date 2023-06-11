#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "WiFi.h"
#include <HTTPClient.h>

const char* ntpServer = "pool.ntp.org";
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
String GOOGLE_SCRIPT_ID = "AKfycbzSRKBIJ2XHJhSkRrEOrCTFH7z0cSuN9hsVyQAAPUbitYUA8pptgAi3qu4jReShoAsooQ";
const char* ssid = "esp";
const char* password = "12345678";
constexpr uint8_t solarPin = 32;
constexpr uint8_t buttonPin = 33;
constexpr uint8_t ledPin = 14;
constexpr uint8_t internal_led = 5;
float solarVoltage = 0;
bool buttonState = LOW;
bool lastButtonState = LOW;
bool ledState = LOW;

unsigned long previousMillis = 0;        // will store the last time the HTTP request was updated
const long interval = 8000;              // interval at which to perform the HTTP request (2 seconds)

void setup() {
  delay(500);
  Serial.begin(9600);
  pinMode(internal_led, OUTPUT);
  digitalWrite(internal_led,HIGH);
  delay(500);
  Serial.println();
  Serial.print("Connecting to wifi: ");
  Serial.println(ssid);
  Serial.flush();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(internal_led,LOW);
    delay(500);
    Serial.print(".");
    digitalWrite(internal_led,HIGH);
  }
  digitalWrite(internal_led,LOW);
  mlx.begin();
  randomSeed(analogRead(0)); // Use an unconnected analog pin for a more random seed.
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, ledState);

}

void loop() {
  buttonState = digitalRead(buttonPin);

  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      ledState = !ledState;
      digitalWrite(ledPin, ledState);
    }
    delay(100); // Debounce delay
    lastButtonState = buttonState;
  }

  solarVoltage = analogRead(solarPin) / 341.3;
  Serial.print(solarVoltage, 2);
  Serial.print(", ");
  Serial.print(ledState);
  Serial.print(", ");
  Serial.print(draw_current(ledState), 2);
  Serial.print(", ");
  Serial.println(mlx.readAmbientTempC(), 2);

  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    String urlFinal = "https://script.google.com/macros/s/"+GOOGLE_SCRIPT_ID+"/exec?"+"solar_voltage=" + String(solarVoltage) + "&current=" + String(draw_current(ledState))+"&temperature=" + String(mlx.readAmbientTempC()) + "&load_status=" + String(ledState);
    Serial.print("POST data to spreadsheet:");
    Serial.println(urlFinal);

    HTTPClient http;
    digitalWrite(internal_led,LOW);
    delay(30);
    digitalWrite(internal_led,HIGH);
    delay(30);
    digitalWrite(internal_led,LOW);
    delay(30);
    digitalWrite(internal_led,HIGH);
    delay(30);
    digitalWrite(internal_led,LOW);

    
    http.begin(urlFinal.c_str());
    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    int httpCode = http.GET(); 
    Serial.print("HTTP Status Code: ");
    Serial.println(httpCode);

    String payload;
    if (httpCode > 0) {
        payload = http.getString();
        Serial.println("Payload: "+payload);
    }
    //---------------------------------------------------------------------
    http.end();
    digitalWrite(internal_led,HIGH);
    delay(40);
    digitalWrite(internal_led,LOW);
    delay(40);
    digitalWrite(internal_led,HIGH);
    delay(40);
    digitalWrite(internal_led,LOW);
    delay(40);
    digitalWrite(internal_led,HIGH);


  }
}

float draw_current(bool ls){
  return ls ? random(1000) / 500.0 + 1.0 : 0.0;  // If ls == true, generate a random float between 1.0 and 3.0. If false, return 0. No need for the map function.
}
