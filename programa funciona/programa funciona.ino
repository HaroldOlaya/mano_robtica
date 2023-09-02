#include <WiFi.h>

const char* ssid = "PC-HAROLD 8023";
const char* password = "8:4a5W85";
int pin1=5;
int pin2=18;
int pin3=2;
int pin4=21;
int pin5=19;

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
 

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  Serial.println("Conectado a la red WiFi");

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {

       String receivedData = "";

    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        
        if (c == '\n') {
          Serial.println(receivedData);
              
          receivedData = ""; // Limpiar la cadena para la próxima lectura
        } else {
          receivedData += c;
        }
             
        int intValue = receivedData.toInt();
        if (intValue<=9){
          switch(intValue){
            case 1:
              digitalWrite(pin1, HIGH); // Encender el LED
              delay(10);// Esperar 1 segundo
              digitalWrite(pin1, LOW);          
              break;
            case 2:
              digitalWrite(pin2, HIGH); // Encender el LED
              delay(10);// Esperar 1 segundo
              digitalWrite(pin2, LOW);          
              break;
            case 4:
              digitalWrite(pin3, HIGH); // Encender el LED
              delay(10);// Esperar 1 segundo
              digitalWrite(pin3, LOW);          
              break;
            case 8:
              digitalWrite(pin4, HIGH); // Encender el LED
              delay(10);// Esperar 1 segundo
              digitalWrite(pin4, LOW);          
              break;
            
          }
        }          
        if (intValue>=10){
          switch(intValue){
            case 16:
            digitalWrite(pin5, HIGH); // Encender el LED
            delay(10);// Esperar 1 segundo
            digitalWrite(pin5, LOW);          
            break;
          }
                                                     
        }                
       
      }
    }
  }
}
