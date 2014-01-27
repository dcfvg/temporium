import processing.video.*;
Capture cam;

int w=1920, h=1080;
int period=50;

void setup() {
  size(w, h, OPENGL);
  camInit(18, false);
}

void draw() {
  
  frameRate(60);
  background(0);

  if (millis()%period < 0) {
    background(255, 0, 0);
    if (cam.available() == true) cam.read();
    delay(1);
    println("capture");
  }
  image(cam, 0, 0);
}

