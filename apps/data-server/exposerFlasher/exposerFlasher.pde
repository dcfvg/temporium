// timer

int fps    = 10, frame = 0;
int phase1 = 60*60*3;

// postion, echelle

float ratiox = 1, ratioy = 1;
int posx = 0, posy = 0, w = 1920, h = 1080, nbImages = 4;

String feedback = "~", imageSet = "exp", lastcapture = "";
// objets

boolean info = true, console = false, fullscreen = true, ispause = false, flash = true, getlastimage = false;

PImage iflash, inega, inoir, img;
boolean sketchFullScreen() {return fullscreen;}

void setup(){
  
  println("<pre>");
  
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
  inega  = loadImage("last.png");
  iflash = loadImage("aquarium-flash-carre.png");
  if(getlastimage) iflash = loadImage("aquarium-flash-fullHD.png");
  inoir  = loadImage("noir.png");
  
  // load first image
  if(getlastimage) refreshlastcapture();
}
void draw(){
  
  background(0);
  // chose image
  
  if ((frame/fps) > phase1 )img = inoir;
  else if (flash)           img = iflash;
  else                      img = inega;
  
  image(img, posx, posy, width/ratiox, height/ratioy);

  if(info) {
    feedback = nf(((frame/fps)/60/60),2)+":"+nf(((frame/fps)/60)%60,2) + ":" +nf((frame/fps)%60,2);    
    text(feedback, 100, 50);
  }
  if(console){
    // contrôle
    println("fps:"+ fps + " fla:" + flash + "    " +(frame%fps) + "/" + (fps) + "   " + frameRate +"fps" );

    // calibrage
    println("x:"+ posx + " y:"+ posy + " rx:"+ ratiox + " ry:"+ ratioy);
    
    // frame
    println("f:"+frame);
  }
  if(!ispause) frame++;  
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
void refreshlastcapture(){
  // scanning imageSet folder with specific paterns
  java.io.File folder = new java.io.File(dataPath(imageSet));
  java.io.FilenameFilter imgExtFilter = new java.io.FilenameFilter() {
    public boolean accept(File dir, String name) {
      return name.toLowerCase().endsWith(".jpg") | name.toLowerCase().endsWith(".jpeg") | name.toLowerCase().endsWith(".png") ;
    }
  };

  String[] filenames = folder.list(imgExtFilter);
  nbImages = filenames.length;
  lastcapture = filenames[nbImages-1];

  inega  = loadImage(imageSet+"/"+lastcapture);
  inega.resize(w, 0);
  inega = inega.get(0, 0, w, h);
  
  inega.filter(GRAY);
  inega.filter(INVERT);
  //inega.filter(DILATE);
  //inega.filter(ERODE);
 
  if(console) { 
    println(nbImages + " layers in " + imageSet);
    println("last : " + lastcapture);
  }
}
