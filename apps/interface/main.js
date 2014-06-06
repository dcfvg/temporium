var fs = require('fs'),
    osc = require('node-osc'),
    util = require('util'),
    ffmpeg = require('fluent-ffmpeg'),
    oscClient = new osc.Client('127.0.0.1', 3334);

module.exports = function(app, io, oscServer){
  console.info('movie <> temporim link initialized');
  
  var capt; // capture programme (bash)
  var spawn = require('child_process').spawn;

  //initClientWindows(); // lauch chrome at launch

  //////////////////////////////
  // server side
  //////////////////////////////
  function initClientWindows(){
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
  function loadScore(){
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

    speed = typeof speed !== 'undefined' ? speed : 1;
    zoom  = typeof zoom  !== 'undefined' ? zoom  : 1;

    var mov_w  = 1920,
        mov_h  = 1037, 
        ratio  = mov_w/mov_h,
        crop_w = Math.round(mov_w*zoom),
        crop_h = Math.round(crop_w/ratio),
        crop_x = Math.round((crop_w - mov_w)/2),
        crop_y = Math.round((crop_h - mov_h)/2),

        proc = new ffmpeg({ source: 'public/exposure/%04d.jpg' })

        .withFps(25)
        .addOptions(['-pix_fmt yuv420p','-c:v libx264', '-preset ultrafast', '-crf 1'])
        .addOptions(['-r 25'])
        .withVideoFilter('scale='+crop_w+':-1')
        .withVideoFilter('crop='+mov_w+':'+mov_h+':'+crop_x+':'+crop_y+'')
        .withVideoFilter('setpts=('+speed+'/1)*PTS')
        .on('end', onRefreshTimelapsEnd)
        .on('error', function(err) { console.log('an error happened: ' + err.message);})
        .saveToFile('public/video/live.mp4');
  };
  function onRefreshTimelapsEnd(){
    console.log('timelapse updated');
    io.sockets.emit("refreshTimelapsEnd");
  };
  function onRefreshTimelaps(param){
    console.log("refreshTimelaps zoom",param[0],"speed",param[1]);
    refreshTimelaps(param[0],param[1]);
  };
  function onCaptureInit(){
    capt = spawn('bash',['bin/capture.sh']);
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
    console.log('kill capture in 2 s');

    setTimeout(function() {
      capt.stdin.pause();
      capt.kill();
    }, 2000);
  }; 
  function onMessage(msg){
    oscClient.send(msg);
  }

  //////////////////////////////
  //  communication 
  //////////////////////////////
  var oscServer = new osc.Server(3333, '0.0.0.0');  
  oscServer.on("message", function (msg, rinfo) {
    console.log(msg);
    io.sockets.emit("oscMessage", msg);
    switch (msg[0]) {
      case "refreshTimelaps":
        refreshTimelaps();
      break;
      case "seance_start":
        //onCaptureInit(); // lanch from client
      break;
      case "captureStop":
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
  });
};