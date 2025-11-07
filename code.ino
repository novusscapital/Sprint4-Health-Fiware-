#include <WiFi.h>
#include <HTTPClient.h>

// ======= CONFIGURAÇÃO DA REDE =======
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// ======= CONFIGURAÇÃO FIWARE =======
// Ajuste o IP e porta conforme o seu IoT Agent
const char* serverUrl = "http://20.63.91.180:7896/iot/d?k=health-api-key&i=dev-esp32-001";

// ======= PINOS =======
#define TEMP_PIN 15     // Sensor analógico de temperatura
#define POT_PIN 13      // Potenciômetro (batimentos)
#define TRIG_PIN 2      // HC-SR04 Trig
#define ECHO_PIN 4      // HC-SR04 Echo

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Conecta Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // ======= 1. TEMPERATURA =======
  int leituraTemp = analogRead(TEMP_PIN);
  // Conversão genérica (0–4095 → 0–3.3V)
  float voltagem = leituraTemp * (3.3 / 4095.0);
  // Supondo sensor analógico linear (TMP36 ou genérico)
  float bodyTemperature = (voltagem - 0.5) * 100.0; // °C aprox.
  bodyTemperature = constrain(bodyTemperature, 30.0, 40.0); // faixa corporal

  // ======= 2. BATIMENTOS (potenciômetro) =======
  int leituraPot = analogRead(POT_PIN);
  // Mapeia 0–4095 → 50–150 bpm
  int heartRate = map(leituraPot, 0, 4095, 50, 150);

  // ======= 3. DISTÂNCIA (HC-SR04) =======
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH);
  float distanciaCm = duracao * 0.034 / 2;
  // Simula distância acumulada em km
  static float distanciaTotal = 0;
  distanciaTotal += distanciaCm / 100000.0; // converte cm → km incremental
  float distanceKm = distanciaTotal;

  // ======= 4. MONITOR SERIAL =======
  Serial.println("==== LEITURAS ATUAIS ====");
  Serial.print("Temperatura: "); Serial.println(bodyTemperature);
  Serial.print("Batimentos: "); Serial.println(heartRate);
  Serial.print("Distância (km): "); Serial.println(distanceKm, 4);
  Serial.println("==========================");

  // ======= 5. ENVIO PARA FIWARE =======
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "text/plain");

    // Formato UL: t|36.7|h|85|d|0.0023
    String payload = "t|" + String(bodyTemperature, 1) +
                     "|h|" + String(heartRate) +
                     "|d|" + String(distanceKm, 4);

    int httpCode = http.POST(payload);

    Serial.print("Enviado → ");
    Serial.println(payload);
    Serial.print("HTTP Code: ");
    Serial.println(httpCode);

    http.end();
  } else {
    Serial.println("Wi-Fi desconectado!");
  }

  delay(5000); // envia a cada 5 segundos
}
