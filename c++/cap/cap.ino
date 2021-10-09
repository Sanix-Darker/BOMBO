/**
 * BOMBO
 * 
 * cap.ino
 * An intelligent 'boite aux lettres' that can notify 
 * when there is new elements in the box !
 * 
 * by d4rk3r
 **/


#include "WiFi.h"
#include "esp_camera.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include "soc/soc.h"           
#include "soc/rtc_cntl_reg.h"
#include "driver/rtc_io.h"
#include <ESPAsyncWebServer.h>
#include <StringArray.h>
#include <SPIFFS.h>
#include <FS.h>
#include <PrintStream.h>

// OV2640 camera module pins (CAMERA_MODEL_AI_THINKER)
// les configs de pins sont presk similaires que ce qui est sur la uno
// Mais Y2_GPIO_NUM m'a poser des soucis chelou
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22
// Photo File Name to save in SPIFFS
#define FILE_PHOTO "/photo.jpg"
// PIN of te Flash light for the camera
#define LED_BUILTIN 4

// The wifi client
WiFiClient client;

// Replace with your network credentials
const char* ssid = "Bbox-B24ECEC6";
const char* password = "KvEuLJhby3Nhdq1Wxm";

// Take new photo boolean
boolean takeNewPhoto = false;

// The html output je vais chou sur la home
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { text-align:center; }
    .vert { margin-bottom: 10%; }
    .hori{ margin-bottom: 0%; }
  </style>
</head>
<body>
  <div id="container">
    <h2>BOMBO</h2>
    <p>It might take more than 5 seconds to capture a photo.</p>
    <p>
      <button onclick="capturePhoto()">CAPTURE</button>
    </p>
  </div>
  <div><img src="photo" id="photo" width="50%"></div>
</body>
<script>
  var deg = 0;
  function capturePhoto() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/capture", true);
    xhr.send();
    setTimeout(function(){
      location.reload();
    }, 3000);
  }
  function isOdd(n) { return Math.abs(n % 2) == 1; }
</script>
</html>)rawliteral";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

void setup() {
  // Serial port for debugging purposes
  Serial.begin(115200);
  
  // We set the flash PINS for the default led mounted on the esp board
  pinMode(LED_BUILTIN, OUTPUT);

  // we lance the wifi connection
  wifiConnect();

  // we set the camera
  setCamera();

  // and we start the 'rest-api'
  startServer();
}

void loop() {
  // We save the photo if takePhoto is ON
  if (takeNewPhoto) {
    capturePhotoSaveSpiffs();
    takeNewPhoto = false;
  }

  // to not brtalize the microcontroller lol
  delay(150);
}
