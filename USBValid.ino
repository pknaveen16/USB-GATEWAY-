#include <WiFi.h>  // Wi-Fi for Pico W
// No pio_usb.h—using serial instead

const char* ssid = "Test";
const char* password = "12345678";
const char* server_ip = "192.168.18.24";  // Laptop IP
const int server_port = 12345;

WiFiClient client;

bool is_usb_safe(String data) {
    if (data.endsWith(".exe") || data.length() > 2000 || data.indexOf("virus") != -1) {
        return false;
    }
    return true;
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("USB Gateway online, you slick fuck!");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWi-Fi: " + WiFi.localIP());
}

void send_alert(String msg) {
    if (client.connect(server_ip, server_port)) {
        client.println(msg);
        client.stop();
    } else {
        Serial.println("Alert failed");
    }
}

void loop() {
    if (Serial.available() > 0) {
        String usb_data = Serial.readStringUntil('\n');
        usb_data.trim();
        Serial.println("Received: " + usb_data);  // Debug
        if (is_usb_safe(usb_data)) {
            Serial.println("Safe: " + usb_data);
        } else {
            Serial.println("Blocked: " + usb_data);
            send_alert("Blocked: " + usb_data);
        }
    }
    delay(10);
}