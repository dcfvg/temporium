import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myBroadcastLocation; 

// timer

int fps    = 10, frame = 0;

// postion, echelle

float ratiox = 1, ratioy = 1;
int posx = 0, posy = 0, w = 1920, h = 1080, nbImages = 4;

String feedback = "~", imageSet = "exp", lastcapture = "";

// objets
boolean fullscreen = false, flash = true;

PImage nega_img, flash_img, img;
boolean sketchFullScreen() {return fullscreen;}

void setup(){
  
  println("<pre>");
  
  // OSC
  oscP5 = new OscP5(this,12000);
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
  
}
void draw(){
  background(0);
  image(img, posx, posy);
  printTimer(); 
}
void oscEvent(OscMessage theOscMessage) {
  
  if (flash) img = iflash;
  else img = inega;
  /* get and print the address pattern and the typetag of the received OscMessage */
  println("### received an osc message with addrpattern "+theOscMessage.addrPattern()+" and typetag "+theOscMessage.typetag());
  theOscMessage.print();
}
void keyPressed(){
  
  // experience control
  
  if( key == 'r') frame  = 0;             // reset experience
  
  if( key == 'g') {                       // flash off
    flash = false;
    if(getlastimage) refreshlastcapture();
  }
  if( key == 'h') flash = true;           // flash on 
  if( key == 't') info = !info;           // show information on projection
  if( key == 'y') console = !console;     // write feedback in console
  if( key == 'p') ispause = !ispause;     // pause experience
  
  // image calibration
  
  if( key == 'n') ratiox = ratiox + 0.01; // change image ratio 
  if( key == 'b') ratiox = ratiox - 0.01; // c   v   |   n   b 
  if( key == 'v') ratioy = ratioy + 0.01; // y+  y-  |   x+  x-
  if( key == 'c') ratioy = ratioy - 0.01; //         |
  
  if( key == 's') posy ++;                // setup position
  if( key == 'z') posy --;                //      z
  if( key == 'd') posx ++;                //    q s d
  if( key == 'q') posx --;                //      -

  // kill
  if( key == 'k') exit();   
}
void img_reload(){
  nega_img  = loadImage("last.png");
  flash_img = loadImage("flash.png");
}
void printTimer(){
  feedback = nf(((frame/fps)/60/60),2)+":"+nf(((frame/fps)/60)%60,2) + ":" +nf((frame/fps)%60,2);    
  text(feedback, 100, 50);
}