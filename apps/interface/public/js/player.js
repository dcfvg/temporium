// sound fix

// test sample :: https://www2.iis.fraunhofer.de/AAC/multichannel.html https://www2.iis.fraunhofer.de/AAC/trouble.html
// js implement :: http://www.html5audio.org/2013/03/surround-audio-comes-to-the-web.html 


/* 

working tests 

http://www.brucewiggins.co.uk/?p=265
http://www.brucewiggins.co.uk/?p=311
http://www.tracktimeaudio.com/?p=635
http://www.axel-hahn.de/demos/html5-audio/tester-audio-formats.php
http://9elements.com/html5demos/audio/

browser support 
http://stackoverflow.com/questions/6762372/html5-audio-what-audio-formats-are-supported

specs
html5 :: https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#AudioDestinationNode

tutorial 

*/


function init() {

  var serverBaseUrl = document.domain,
      socket = io.connect(serverBaseUrl),
      sessionId = '',
      $movie = $("#movie"),
      $life  = $("#life"),
      $pop_movie = Popcorn("#movie"),
      $pop_life = Popcorn("#life"),
      started=false,
      score;
    
  /* sockets */

  socket.on('connect', onSocketConnect);
  socket.on('oscMessage', onSocketOscMessage);
  socket.on('score', onSocketScore);

  function onSocketConnect() {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);
    socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  function onSocketOscMessage(obj){
    console.log(obj);

    switch (obj[0]) {
      case "/seance_start":
        console.log("session start");
        showMovie();
      break;
      case "/life_reload":
        reloadLife();
      break;
      case "/image_formation":
        if(!started && parseInt(obj[1]) > 15){
          started = true;
          showMovie();
        }
      break;
      case "/player_jump":
        $pop_movie.currentTime( obj[1] ).play();
      break;
      case "/player_reset":
        reset();
      break;
      
      default:
        text ="hein ?";
    };
  };
  function onSocketScore(obj){
    score = obj[1];
    console.log(score);
  };
  
  /* 
  // http://popcornjs.org/popcorn-docs/getting-started/
  // http://jsfiddle.net/popcornjs/G3Csf/
  // https://www.npmjs.org/package/osc.io
  */

  // functions
  
  function showMovie(){
    $movie.removeClass("off");
    $life.addClass("off");
    $pop_movie.play();
  }
  function showLife(){
    $life.removeClass("off");
    $movie.addClass("off");
    $pop_life.play();
  }
  function reloadLife(){
    // add reload argument to avoid cache
    $life.attr("src","life.mp4?reload="+Math.round((new Date()).getTime() / 1000)).load();
  }
  function blackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  }
  function getScore(){
    socket.emit('getScore',true);
  }
  function reset (){
    console.log("reset player");
    blackScreen();
    getScore();
    
    started=false;
    
    // seek to beginning 
    $pop_movie.pause().currentTime(0);  
    $pop_life.pause().currentTime(0);
  }

  // movie event creation 
  // http://stackoverflow.com/questions/14573407/iterate-over-cue-method-with-popcorn-js

  $pop_movie.cue( 4, function() {
      console.log("cut vivant 1");
      //$pop_life.currentTime( 35 );
      //showLife();
      //$pop_movie.currentTime( 80 ).pause();
  });

  // players events 
  $pop_life.on("ended", function() {
    $pop_movie.play();
    showMovie();
  });
  $pop_movie.on("ended", function() {
      console.log("seance_end ! ");
      reset();
      socket.emit('1', '/seance_end');
  });
  
  getScore();

  // dev shortcuts
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
};
$(document).on('ready', init);