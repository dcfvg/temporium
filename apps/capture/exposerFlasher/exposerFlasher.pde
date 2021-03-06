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
boolean fullscreen = true, flash = true, liveMode = false;
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
}
boolean sketchFullScreen() {return fullscreen;}
void draw(){
  
  // reset image
  background(0);
  
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

  if(theOscMessage.checkAddrPattern("/EF")==true) {
    
    String o = theOscMessage.get(0).stringValue();
    
         if(o.equals("expose"))        img = nega_img;      // swith to nega
    else if(o.equals("flash"))         img = flash_img;     // switch to flash
    else if(o.equals("imgReload"))     img_reload();        // refresh image
    else if(o.equals("kill"))          exit();              // stop application
    else if(o.equals("resetTime"))     frame  = 0;          // reset timer
    
    //println(o);
    
    return;
  }
}
void img_reload(){
  /**
   * refresh image from 'data' folder
   *
   */
  
  nega_img  = loadImage("nega.png");
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
