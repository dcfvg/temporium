/**
 *  Exposer Flash
 *  Alterne l'exposition d'un négatif ( nega ) avec un flash
 *  L'application répond à des ordres OSC
 *  
 *  l'image à projeter ( néga ) 
 *  est prise dans le dossier data ( nega.png ) 
 *  
 *  ou filmée en temps réel ( liveMode )
 *
 *  @author Benoît VERJAT
 *  @since  01.04.2013
 */

// OSC listener 

import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myBroadcastLocation; 

// get webcam
import processing.video.*;
Capture video;

// timer text
String timer = "~";

// images ( nega: the picture to expose, flash: the flash , img the actual state of projection )
PImage nega_img, flash_img, img; 

// param
boolean fullscreen = false, flash = true, liveMode = true;
int fps = 10, frame = 0, w = 1920, h = 1080;

void setup(){
  
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
  
  // liveMode 
  if(liveMode){
    video = new Capture(this, 1920, 1080);
    video.start();
  }
}
boolean sketchFullScreen() {return fullscreen;}
void draw(){
  
  // reset image
  background(0);
  
  // if live mode enable nega_img is the webcam image
  if(liveMode){
    video.loadPixels();
    nega_img = video;
  }
  
  // print image
  image(img, 0, 0);
  
  // add timer
  printTimer();
  
  // frame count for timer
  frame++;
}
void oscEvent(OscMessage theOscMessage) {
  
  /**
   * wait for OSC events
   *
   */

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
  /**
   * refresh image from 'data' folder
   *
   */
  
  nega_img  = loadImage("last.png");
  flash_img = loadImage("flash.png");
}
void printTimer(){
  /**
   * calculate experience time and display it
   *
   */
  timer = nf(((frame/fps)/60/60),2)+":"+nf(((frame/fps)/60)%60,2) + ":" +nf((frame/fps)%60,2);    
  text(timer, 100, 50);
}
void captureEvent(Capture c) {
  /**
   * on live mode, read webcam image
   */
   
  if(liveMode) c.read();
}