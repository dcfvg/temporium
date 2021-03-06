var fs = require('fs'),
    osc = require('node-osc'),
    util = require('util'),
    ffmpeg = require('fluent-ffmpeg'),
    oscClient = new osc.Client('127.0.0.1', 3334);

module.exports = function(app, io, oscServer){
  console.info('movie <> temporim link initialized');
  
  var capt; // capture programme (bash)
  var spawn = require('child_process').spawn;

  initClientWindows(); // lauch safari at launch

  //////////////////////////////
  // server side
  //////////////////////////////
  function initClientWindows(){

    //lancement du script qui lance chrome et chrome canary en FS sur chacun des écrans
    //cf. bin/initClientWindows.sh

    clientWindows = spawn('bash',['bin/initClientWindows.sh']);

    clientWindows.stdout.on('data', function (data) {
      console.log('stdout: ' + data);
    });
    clientWindows.stderr.on('data', function (data) {
      console.log('stderr: ' + data);
    });
    clientWindows.on('exit', function (code) {
      console.log('child process exited with code ' + code);
    });
  };

  function onFullScreen(){
    fullScreen = spawn('bash',['bin/safariFullScreen.sh']);

    fullScreen.stdout.on('data', function (data) {
      console.log('stdout: ' + data);
    });
    fullScreen.stderr.on('data', function (data) {
      console.log('stderr: ' + data);
    });
    fullScreen.on('exit', function (code) {
      console.log('child process exited with code ' + code);
    });
  };

  function loadScore(){

    // le "score" contiens les moments clefs du montage et les actions associés 
    // cf. /public/score.csv

    var Converter=require("csvtojson").core.Converter;
    var fs=require("fs");

    var csvFileName="./public/score.csv";
    var fileStream=fs.createReadStream(csvFileName);
    var csvConverter=new Converter({constructResult:true});

    csvConverter.on("end_parsed",function(jsonObj){
      io.sockets.emit("score", jsonObj);
    });
    //read from file
    fileStream.pipe(csvConverter);
  };

  //////////////////////////////
  //  movies Management
  //////////////////////////////
  function refreshTimelaps( speed, zoom){

    // compilation de la video "live" à partir des JPEG pris par l'appareil photo

    speed = typeof speed !== 'undefined' ? speed : 1;
    zoom  = typeof zoom  !== 'undefined' ? zoom  : 1;

    var mov_w  = 1920,
        mov_h  = 1037, 
        ratio  = mov_w/mov_h,
        crop_w = Math.round(mov_w*zoom),
        crop_h = Math.round(crop_w/ratio),
        //crop_x = Math.round((crop_w - mov_w)/2),
        //crop_y = Math.round((crop_h - mov_h)/2),
        crop_x = crop_w - mov_w, //nbpixels*crop_w
        crop_y = 0, //nbpixels*crop_h
        speedTransfo = 1+(speed - 1)/7,

        proc = new ffmpeg({ source: 'public/exposure/%04d.jpg' })

        .withFps(25)
        //crf valeur à modifier si l'on veut que la vidéo se compile plus rapidement. On agit ici sur la compression et la qualité de la vidéo.
        .addOptions(['-pix_fmt yuv420p','-c:v libx264', '-preset ultrafast', '-crf 22'])
        .addOptions(['-r 25'])
        .withVideoFilter('scale='+crop_w+':-1')
        .withVideoFilter('crop='+mov_w+':'+mov_h+':'+crop_x+':'+crop_y+'')
        .withVideoFilter('setpts=(1*'+speedTransfo+')*PTS')
        .on('end', onRefreshTimelapsEnd)
        .on('error', function(err) { console.log('an error happened: ' + err.message);})
        .saveToFile('public/video/live.mp4');
  };
  function onRefreshTimelapsEnd(){
    console.log('timelapse updated');
    io.sockets.emit("refreshTimelapsEnd");
  };
  function onRefreshTimelaps(param){
    console.log("refreshTimelaps zoom",param[1],"speed",param[0]);
    refreshTimelaps(param[0],param[1]);
  };
  function onCaptureInit(){
    capt = spawn('bash',['bin/capture.sh']);
    console.log("Lancé");
    capt.stdout.on('data', function (data) {
      console.log('stdout: ' + data);
    });
    capt.stderr.on('data', function (data) {
      console.log('stderr: ' + data);
    });
    capt.on('exit', function (code) {
      console.log('child process exited with code ' + code);
    });
  };
  function onCaptureStop (){
    //use ps in terminal for idetifying the process
    // quitter node ne quite pas les processus qui ont été "spawné"
    // cette commande permet de killer la capture.

    console.log('kill capture in 2 s');

    setTimeout(function() {
      capt.stdin.pause();
      capt.kill();
    }, 2000);

  }; 
  function onMessage(msg){
    //adding "/" here for all osc messages
    oscClient.send("/"+ msg, "1");

  };
  function onLastSequence(){
    io.sockets.emit("expose_stop", true);
  };

  //////////////////////////////
  //  communication 
  //////////////////////////////
  var oscServer = new osc.Server(3333, '0.0.0.0');  
  oscServer.on("message", function (msg, rinfo) {
    console.log(msg);
    io.sockets.emit("oscMessage", msg);
    switch (msg[0]) {
      case "/refreshTimelaps":
        refreshTimelaps();
      break;
      //function to stop the film :
      case "/seance_stop":
        onCaptureStop();
      break;
      case "/capture_stop":
        onCaptureStop();
      break;
    };
  });
  io.on("connection", function(socket){
    socket.on("message", onMessage);
    socket.on("getScore", loadScore);
    socket.on("refreshTimelaps", onRefreshTimelaps);
    socket.on("captureStop", onCaptureStop);
    socket.on("captureInit", onCaptureInit);
    socket.on("fullScreen", onFullScreen);
    socket.on("last_sequence", onLastSequence);
  });
};