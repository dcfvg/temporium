var fs = require('fs');

var osc = require('node-osc');
var util = require('util');


var oscClient = new osc.Client('127.0.0.1', 3334);

module.exports = function(app, io, oscServer){
  console.log("main module initialized");

  function loadScore(){
    //Converter Class
    var Converter=require("csvtojson").core.Converter;
    var fs=require("fs");

    var csvFileName="./public/score.csv";
    var fileStream=fs.createReadStream(csvFileName);
    //new converter instance
    var csvConverter=new Converter({constructResult:true});

    //end_parsed will be emitted once parsing finished
    csvConverter.on("end_parsed",function(jsonObj){
       //console.log(jsonObj); //here is your result json object
       io.sockets.emit("score", jsonObj);
    });

    //read from file
    fileStream.pipe(csvConverter);
  }

  var util  = require('util'),
      spawn = require('child_process').spawn;


  var oscServer = new osc.Server(3333, '0.0.0.0');
  
  oscServer.on("message", function (msg, rinfo) {
    console.log(msg);
    io.sockets.emit("oscMessage", msg);


    /// SPAWN TEST 

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

  });

  /**
  * Socket.IO events
  */

  io.on("connection", function(socket){
    socket.on("message", function(obj) {
      console.log(obj);
      oscClient.send(obj);
    });
    socket.on("getScore", function(obj){
      loadScore();
    });
  });
};