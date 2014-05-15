var express = require("express");
var app     = express();
var http    = require("http").createServer(app);
var io      = require("socket.io").listen(http);
// var readDir = require('readdir');

var main    = require('./main');
var config  = require('./config');
var router  = require('./router');

var m = new main(app, io);


// osc
var osc = require('node-osc');
var util = require('util');


// var client = new osc.Client('127.0.0.1', 3334);
// client.send('/test', 1, 1, 2, 3, 5, 8);


var oscServer = new osc.Server(3333, '0.0.0.0');
oscServer.on("message", function (msg, rinfo) {
    console.log("Message:");
    console.log(msg);
    io.sockets.emit("message", msg);
});



/*
* Server config
*/
config(app, express);

/**
* Server routing and io events
*/
router(app, io, m);

/**
* Start the http server at port and IP defined before
*/
http.listen(app.get("port"), app.get("ipaddr"), function() {
  console.log("Server up and running. Go to http://" + app.get("ipaddr") + ":" + app.get("port"));
});
