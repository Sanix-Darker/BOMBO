/**
 * BOMBO
 * 
 * Collections of all functions/utils for wifi
 * wifi.ino
 * 
 * by d4rk3r
 **/


/**
 * wifi_connect is a method to connect that allow BOMBO to connect 
 * to the wifi
 **/
void wifiConnect() {
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1700);
        Serial << "Connecting to WiFi..." << endl;
    }
    if (!SPIFFS.begin(true)) {
        Serial << "An Error has occurred while mounting SPIFFS" << endl;
        ESP.restart();
    }
    else
        Serial << "SPIFFS mounted successfully" << endl;

    // Print ESP32 Local IP Address
    Serial << "IP Address: http://" << WiFi.localIP() << endl;

    // Turn-off the 'brownout detector'
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
}
