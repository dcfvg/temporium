var fs = require('fs');

var osc = require('node-osc');
var util = require('util');


var oscClient = new osc.Client('127.0.0.1', 3334);

module.exports = function(app, io){
  console.log("main module initialized");
  
  function init(){
  };
  /**
  * Socket.IO events
  */
  io.on("connection", function(socket){

    socket.on("message", function(obj) {
      console.log(obj);
      oscClient.send(obj);
    });

    /*
      When a new user connects to our server, we expect an event called "newUser"
      and then we'll emit an event called "newConnection" with a list of all
      participants to all connected clients
    */
    socket.on("newUser", function(data) {
      // participants.push({id: data.id, name: data.name});
      // io.sockets.emit("newConnection", {participants: participants});
    });

    /*
      When a user changes his name, we are expecting an event called "nameChange"
      and then we'll emit an event called "nameChanged" to all participants with
      the id and new name of the user who emitted the original message
    */
    socket.on("nameChange", function(data) {
      // _.findWhere(participants, {id: socket.id}).name = data.name;
      // io.sockets.emit("nameChanged", {id: data.id, name: data.name});
    });

    /*
      When a client disconnects from the server, the event "disconnect" is automatically
      captured by the server. It will then emit an event called "userDisconnected" to
      all participants with the id of the client that disconnected
    */
    socket.on("disconnect", function() {
      // participants = _.without(participants,_.findWhere(participants, {id: socket.id}));
      // io.sockets.emit("userDisconnected", {id: socket.id, sender:"system"});
    });
  });

  init();
};
