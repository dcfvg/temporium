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

import processing.video.*;
import oscP5.*;
import netP5.*;

Movie mainMov;  // the entire movie
Movie liveMov;  // the live timelaps
Movie projMov;  // the live timelaps

OscP5 oscP5;
NetAddress myBroadcastLocation; 

// params
boolean fullscreen = false, live1_loaded;
int fps = 50, w = 1920, h = 1080;
float cuePoint1 = 8.500;


void setup() {
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

  mainMov = new Movie(this, "film.mp4");
  mainMov.play();
}
boolean sketchFullScreen() {return fullscreen;}

void draw() {
  background(255);

  float md = mainMov.duration();
  float mt = mainMov.time();


  if(mt > cuePoint1){
    if (liveMov.available()) liveMov.read();
    projMov = liveMov;

  }else{
    if (mainMov.available()) mainMov.read();
    projMov = mainMov;
  }


  image(projMov, 0, 0, w, h);

  text(mt, 100, 50);

  if (mt > cuePoint1 - 2 || !live1_loaded) {
    liveMov = new Movie(this, "timelaps.mp4");
    live1_loaded = true;
    liveMov.play();
    mainMov.pause();
  }

}
void oscEvent(OscMessage theOscMessage) {
  
  /**
   * wait for OSC events
   *
   */

  if(theOscMessage.checkAddrPattern("/exposeFlashCommander")==true) {
    
    String o = theOscMessage.get(0).stringValue();
    
         if(o.equals("PR_start"))  mainMov.play();
    else if(o.equals("PR_reset"))  mainMov.jump(0);
    
    println(o);
    
    return;
  }
}

