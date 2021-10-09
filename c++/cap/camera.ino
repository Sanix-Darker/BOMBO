/**
 * BOMBO
 * 
 * Collections of all functions/utils for the camera part on the esp
 * camera.ino
 * 
 * by d4rk3r
 **/


/**
 * We set the Camera
 **/
void setCamera(){
  // We set configutrations for the camera
  camera_config_t config;

  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial << "Camera init failed with error 0x" << err;
    ESP.restart();
  }
}

// Check if photo capture was successful
// We just chef if the file-size is upper than 100
bool checkPhoto( fs::FS &fs ) {
  File f_pic = fs.open( FILE_PHOTO );
  return ( f_pic.size() > 100 );
}

// We save the photo to the disk (la carte SD)
void savePhoto(camera_fb_t* fb){
  // Photo file name
  Serial << "Picture file name: \n" << FILE_PHOTO;
  File file = SPIFFS.open(FILE_PHOTO, FILE_WRITE);

  // Insert the data in the photo file
  if (!file)
    Serial << "Failed to open file in writing mode" << endl;
  else {
    file.write(fb->buf, fb->len); // payload (image), payload length
    // serial as cout print
    Serial << "File: " << FILE_PHOTO << " saved - Size: " << file.size() << " bytes" << endl;
  }
  // Close the file
  file.close();
}

// The capture process for taking a real photo
camera_fb_t* capture(){
  camera_fb_t *fb = NULL; // pointer
  // the file bin capture
  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return NULL;
  }

  return fb;
}

// Capture Photo and Save it to SPIFFS
void capturePhotoSaveSpiffs( void ) {
  // We start the flash light
  digitalWrite(LED_BUILTIN, HIGH);
  do {
    // Take a photo with the camera
    Serial << "Taking a photo..." << endl;
    
    // Take a picture
    camera_fb_t *fb = capture();

    // We save the photo to the disk
    savePhoto(fb);
    // we clean stuffs
    esp_camera_fb_return(fb);

    // we delay the saving process
    delay(5);
    // Boolean indicating if the picture has been taken correctly
    // check if file has been correctly saved in SPIFFS
  } while ( !checkPhoto(SPIFFS) );
  // We stop the flash light
  digitalWrite(LED_BUILTIN, LOW);
}
