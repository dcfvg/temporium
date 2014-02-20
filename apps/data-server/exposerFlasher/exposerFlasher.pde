import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myBroadcastLocation; 

int fps = 10, frame = 0, w = 1920, h = 1080;
String timer = "~";
boolean fullscreen = false, flash = true;
PImage nega_img, flash_img, img;

boolean sketchFullScreen() {return fullscreen;}

void setup(){
  
  println("<pre>");
  
  // OSC
  oscP5 = new OscP5(this,4242);
  myBroadcastLocation = new NetAddress("127.0.0.1",4242);
  
  // ui
  size(w,h); 
  background(0);
  frameRate(fps);
  noCursor();
  
  // typo
  textFont(createFont("Monaco", 24));
  fill(#FFFFFF);
  textAlign(LEFT);

  // images
  img_reload();
  img = flash_img;
}
void draw(){
  background(0);
  image(img, posx, posy);
  printTimer();
  frame++;
}
void oscEvent(OscMessage theOscMessage) {
  if(theOscMessage.checkAddrPattern("/exposeFlashCommander")==true) {
    
      String o = theOscMessage.get(0).stringValue();
      
           if(o.equals("expose"))        img = nega_img;      // swith to nega
      else if(o.equals("flash"))         img = flash_img;     // switch to flash
      else if(o.equals("img_reload"))    img_reload();        // refresh image
      else if(o.equals("kill"))          exit();              // stop application
      else if(o.equals("reset_time"))    frame  = 0;          // reset timer
      println(o);
      
      return;
  }
}
void img_reload(){
  nega_img  = loadImage("last.png");
  flash_img = loadImage("flash.png");
}
void printTimer(){
  timer = nf(((frame/fps)/60/60),2)+":"+nf(((frame/fps)/60)%60,2) + ":" +nf((frame/fps)%60,2);    
  text(timer, 100, 50);
}