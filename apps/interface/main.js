var fs = require('fs'),
    osc = require('node-osc'),
    util = require('util'),
    ffmpeg = require('fluent-ffmpeg'),
    oscClient = new osc.Client('127.0.0.1', 3334);

module.exports = function(app, io, oscServer){
  console.log("movie <> temporim link initialized");

  //////////////////////////////
  // dynamic editing
  //////////////////////////////
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
  }

  //////////////////////////////
  //  movies Management
  //////////////////////////////
  function refreshTimelaps( speed, zoom){

    speed = typeof speed !== 'undefined' ? speed : 1;
    zoom  = typeof zoom  !== 'undefined' ? zoom  : 1;

    var mov_w  = 1888,
        mov_h  = 1062, 
        ratio  = mov_w/mov_h,
        crop_w = Math.round(mov_w*zoom),
        crop_h = Math.round(crop_w/ratio),
        crop_x = Math.round((crop_w - mov_w)/2),
        crop_y = Math.round((crop_h - mov_h)/2),
        proc = new ffmpeg({ source: 'public/exposure/im%04d.jpg' })

        .withFps(25)
        .addOptions(['-pix_fmt yuv420p','-c:v libx264', '-preset ultrafast', '-crf 1'])
        .addOptions(['-r 25'])
        .withVideoFilter('scale='+crop_w+':-1')
        .withVideoFilter('crop='+mov_w+':'+mov_h+':'+crop_x+':'+crop_y+'')
        .withVideoFilter('setpts=('+speed+'/1)*PTS')
        .on('end', onRefreshTimelapsEnd)
        .on('error', function(err) { console.log('an error happened: ' + err.message);})
        .saveToFile('public/video/live.mp4');
  }
  function onRefreshTimelapsEnd(){
    console.log('timelapse updated');
  }
  function initCapture(){

    /// SPAWN TEST 
    spawn = require('child_process').spawn;
    capt = spawn('bash',['bin/test.sh']); 
    capt.stdout.on('data', function (data) {    // register one or more handlers
      console.log('stdout: ' + data);
    });
    capt.stderr.on('data', function (data) {
      console.log('stderr: ' + data);
    });
    capt.on('exit', function (code) {
      console.log('child process exited with code ' + code);
    });

    setTimeout(function() {
      console.log('kill');
      capt.stdin.pause();
      capt.kill();
    }, 10000);

    /// END SPAWN TEST
  }

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
    };
  });

  io.on("connection", function(socket){
    socket.on("message", oscClient.send);
    socket.on("getScore", loadScore);
    socket.on("refreshTimelaps", refreshTimelaps);
  });
};