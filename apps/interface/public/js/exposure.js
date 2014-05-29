function init() {

  var serverBaseUrl = document.domain,
      socket = io.connect(serverBaseUrl),
      sessionId = '',
      $nega = $("#nega");

  //sockets
  socket.on('connect', onSocketConnect);
      
  // functions
  function reloadNega(){
    $nega.attr("src","/images/nega.png?reload="+Math.round((new Date()).getTime() / 1000)).load();
  }
  function expose(){
    $nega.removeClass("off");
  }
  function flash(){
    $nega.addClass("off");
  }
  function onSocketConnect() {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);
    socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  // OSC
  socket.on('oscMessage', function(obj){
    switch (obj[0]){
      case "/EF": // check patern
        console.log(obj[1]);

        switch (obj[1]) { // check message
          case "expose":
            expose();
          break;
          case "flash":
            flash();
          break;
          case "imgReload":
            reloadNega();
          break;
        };
      break;
    }
  });
  // shortcuts
  $(document).keypress(function( event ){
    // console.log(event.which);
    if ( event.which == 101 ) expose();       //e -> expose
    if ( event.which == 102 ) flash();        //f -> flash 
    if ( event.which == 114 ) reloadNega();   //r -> reload 
  });

  // reset();
};
$(document).on('ready', init);