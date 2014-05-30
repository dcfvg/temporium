function init() {

  var serverBaseUrl = document.domain;
  var socket = io.connect(serverBaseUrl);
  var sessionId = '';

  //sockets

  socket.on('connect', onSocketConnect);
  function onSocketConnect() {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);
    socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };


  var $nega = $("#nega");
      
  // functions
  function reloadNega(){
    // add reload argument to avoid cache
    $nega.attr("src","/images/image_vivante.jpg?reload="+Math.round((new Date()).getTime() / 1000)).load();
  }

  // OSC
  socket.on('oscMessage', function(obj){

    switch (obj[0]){
      case "/seance_start":
        console.log("starting sequence");
      break;
      case "/EF": // check patern
        console.log(obj[1]);

        switch (obj[1]) { // check message
          case "expose":
            $nega.removeClass("off");
          break;
          case "flash":
            $nega.addClass("off");
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
    //console.log(event.which);

    //m -> movie
    if ( event.which == 109 ) showMovie(); 
    
    //l -> life
    if ( event.which == 108 ) showLife();
    
    //r -> refreshlife
    if ( event.which == 114 ) reloadLife();
    
    // s -> seek 
    if ( event.which == 115 ) {
        // $pop_movie.currentTime( 1 ).play();
        $pop_life.playbackRate(3).play(); // change player speed
        socket.emit('message', '/test');
    };
  });

  // reset();
};
$(document).on('ready', init);