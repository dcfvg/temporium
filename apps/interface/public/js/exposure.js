function init() {

  var socket = io.connect("http://localhost:8080"),
      $nega = $("#nega");

  //Délai de sécurité en ms
  var delayExposure = 250;

  //sockets
  socket.on('connect', onSocketConnect);
      
  // functions
  function reloadNega(){
    $nega.attr("src","/images/nega.png?reload="+Math.round((new Date()).getTime() / 1000)).load();
  }
  function expose(){
    setTimeout(function(){
      $nega.removeClass("off");
    },delayExposure);
  }
  function flash(){
    $nega.addClass("off");
  }
  function onSocketConnect() {
    console.log('Connected');
    //socket.emit('newUser', {name: $('#name').val()});
  };
  function onSeanceEnd(){
    setTimeout(function(){
          
       $nega.addClass("off");

      },5000);
    
  };

  socket.on('expose_stop', onSeanceEnd);

  // OSC
  socket.on('oscMessage', function(obj){
    console.log(obj[0]);
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
      case "/seance_end":
        onSeanceEnd();
      break;
      case "/seance_stop":
        onSeanceEnd();
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