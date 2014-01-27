void camInit(int idCam, boolean list) {
  String[] cameras = Capture.list();

  if (cameras.length == 0) {
    println("There are no cameras available for capture.");
    exit();
  } 
  else {
    if (list) println("Available cameras:");
    if (list) for (int i = 0; i < cameras.length; i++) println(i+":"+cameras[i]);
    
    cam = new Capture(this, cameras[idCam]);
    cam.start();
  }
}

