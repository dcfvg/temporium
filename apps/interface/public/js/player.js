function init() {

  //////////////////////////////
  // vars
  //////////////////////////////
  var socket = io.connect("http://localhost:8080"),
      $d = $(document)
      ;
  //temps d'attente en seconde avant de lancer le film aprrès FlasherExposer
  var delay = 500;

  var $movie            = $("#movie"),                  // container
      movieUrl          = "/video/immersion.mov",
      movieWidth        = 1920, movieHeight = 1036,     // size to display
      movieGoesOn       = false,                        // 
      movieCurentStep   = 0,                            // current event step
      movieWatchInteval = 500,                          // timecode events refresh frequency
      movieStartMargin  = 44,
      movieVolume       = 0.5,
      $pop_movie	= Popcorn("#movie")
      ;

  $pop_movie.on('error'         , onPlayerEvent);
  $pop_movie.on('pause'         , onPlayerEvent);
  $pop_movie.on('suspend'       , onPlayerEvent);
  $pop_movie.on('ended'         , onMovieEnded);
  $pop_movie.on('canplay'       , onPlayerEvent);
  $pop_movie.on('canplaythrough', onCanPlayThrough);

  var $life             = $("#life"),
      lifeUrl           = "/video/live.mp4",
      $pop_life         = Popcorn("#life")
      ;

  var $timer        = $("#timer");

  var image_formation = 20,
      compileDelay = 90,
      decideDelay = 2,
      canPlay = false;

      ;
 
  //////////////////////////////
  // On
  //////////////////////////////

  socket.on('connect', onSocketConnect);
  socket.on('oscMessage', onSocketOscMessage);
  socket.on('score', onSocketScore);
  socket.on('refreshTimelapsEnd', onRefreshTimelapsEnd); 
  
  $d // on
    .on( "seance_start"     , onSeanceStart)
    .on( "seance_stop"      , onMovieEnded)
    .on( "capture_stop"     , onMovieEnded)
    .on( "lifeRefreshMovie" , onReloadLife)
    .on( "image_formation"  , onImageFormation)
    .on( "player_reset"     , reset)
    .on( "showMovie"        , onShowMovie)
    .on( "showLife"         , onShowLife)
    .on( "projectionStart"  , onProjectionStart)
    .on( "timerWait"        , onTimerWait)
  ;
  
  $pop_life.on("ended",onLifeEnded);

  // dev shortcuts
  $d.keypress(function( event ){
    //console.log(event.which);
    if ( event.which == 109 ) $d.trigger("showMovie");  // m
    if ( event.which == 108 ) $d.trigger("showLife");   // l
    if ( event.which == 114 ) $d.trigger("reloadLife"); // r
    if ( event.which == 104 ) { // h
      var time = getCurrentTime();
      $pop_movie.currentTime(time + 10);
      console.log("jump +10s -> "+getCurrentTime());
    };
    if ( event.which == 106 ) { // j
      var time = getCurrentTime();
      $pop_movie.currentTime(time + 30);
      console.log("jump +30s -> "+getCurrentTime());
    };

    if ( event.which == 107 ) { console.log("t :",getCurrentTime());}// k
    if(event.which == 103){
      $pop_movie.play(0); //g
    };
    if(event.which == 102){
      $pop_movie.pause(); //f
    };
  });

  //////////////////////////////
  // HANDLERS 
  //////////////////////////////

  // messages events
  function onSocketConnect() {
    console.log('Connected ');
    //socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  function onSocketOscMessage(obj){
    // conversion d'un event OSC -> IO en javascript chez le client 
    $d.trigger(obj[0].replace("/",""),[ obj[1] ]);
  };
  function onSocketScore(obj){
    // le "score" à été rechargé
    score = obj;
    console.log(obj);
  };

  // seance == top vivant
  function onSeanceStart(){
    console.log("# seance seance_start !");    
    socket.emit('captureInit',true);
    socket.emit('fullScreen',true);
    $timer.removeClass("off");
    $d.trigger("timerWait");
    
    setTimeout(function(){
   
      $d.trigger("projectionStart"); 

    },delay*1000);
    
  };
  // projection == film
  function onProjectionStart(){
    
    console.log("# projection !");

    $timer.addClass("off");
    
    $pop_movie.play(0);

    $d.trigger("showMovie");

    movieGoesOn = true;

    movieCurentStep = 0;
    setNextStep();
    setVolume(movieVolume);
  }

  // player events
  function onImageFormation(e, obj){

    image_formation = parseInt(obj);
    console.log('image_formation updt',image_formation);

  };
  function onReloadLife(){
    // add reload argument to avoid cache
    if($life.hasClass("off")){
      //$pop_life.load();
      $life.attr("src",lifeUrl+ "?" + Math.round((new Date()).getTime() / 1000)).load();
    };
  };
  function onRefreshTimelapsEnd (obj) {
    console.log('~ life render finished !');
    $d.trigger("lifeRefreshMovie");
  };
 
  // movies action
  function onShowMovie(){
    
    $movie.removeClass("off");
    $life.addClass("off");
    $d.trigger("lifeRefreshMovie");

    console.log("Movie !!!");
  };
  
  function onShowLife(){
    $movie.addClass("off");
    $life.removeClass("off");

    setTimeout(function(){
      $pop_life.play(0);
    },1000);    
    
    console.log("Life !!!");    
  };

  function onBlackScreen(){
    $timer.addClass("off");
    $life.addClass("off");
    $movie.addClass("off");
  };

  //////////////////////////////
  // Helpers
  //////////////////////////////

  function getScore(){
    socket.emit('getScore',true);
  };
  function getAt(l){
    return (parseInt(l.at_sec)); 
  };
  function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  function setVolume(v){
    $pop_movie.volume(v);
  };
  function getCurrentTime(){
    return $pop_movie.currentTime();
  };

  function onPlayerEvent(ev){
    //console.log("Event :: " + ev.type);    
  };
  function onCanPlayThrough(){
    $("#wait").addClass('off');

    movieDuration  = $pop_movie.duration();

    //emulateImageFormation(60);

    console.log("movie is ready !", movieDuration);
  };
  function onMovieEnded(){

    console.log("movie end");
    socket.emit('fullScreen',true);
    socket.emit('message', "seance_end" , true);

    reset();
  };

  //////////////////////////////
  // actions
  //////////////////////////////

  function reset(){
    console.log("reset player");

    onBlackScreen();
    getScore();

    //socket.emit('refreshTimelaps');

    movieGoesOn = false;

    // seek to beginning 

    $pop_movie.pause().currentTime(0);
  
    $pop_life.pause().currentTime(0);

    //$pop_life.pause().currentTime(0);
  };
  function getJumpIn(step){
    var jump_max = step.jump_max;
    var movieProgress  = Math.round((getCurrentTime()/movieDuration)*100);
    var lifeProgress = image_formation; //Math.round((image_formation/255)*100);
    var jump = (jump_max/2)-(((lifeProgress - movieProgress)/100)*jump_max);

    if(jump > jump_max) {
      jump = jump_max - 0,01;
    }; // to FIX 

    if(jump < 0) {
      jump = 0,01;
    };

    console.log(step.type,'jump = ',jump,'/',jump_max,' (film :',movieProgress,'% ',' life :',lifeProgress,'%)');
    return jump;
  };

  function getJumpOut(step){
    var jump_max = step.jump_max;
    var movieProgress  = Math.round((getCurrentTime()/movieDuration)*100);
    var lifeProgress = image_formation; //Math.round((image_formation/255)*100);
    var jump = (jump_max/2)+(((lifeProgress - movieProgress)/100)*jump_max);

    if(jump > jump_max) {
      jump = jump_max - 0,01;
    }; // to FIX 

    if(jump < 0) {
      jump = 0,01;
    };

    console.log(step.type,'jump = ',jump,'/',jump_max,' (film :',movieProgress,'% ',' life :',lifeProgress,'%)');
    return jump;
  };

  function setNextStep(){
    var step = score[movieCurentStep],
        at = getAt(step),
        renderStarted = false,
        decideStarted = false,
        jump
        ;

    console.log("~ waiting", step.id, step.title, '(', step.type, ')', "@", at);

    var inter = setInterval(function(){

      t = getCurrentTime();

      // TIMELAPS COMPILATION
      if(t > (at - compileDelay) && !renderStarted){
        renderStarted = true;
        socket.emit('refreshTimelaps',[step.life_speed, step.life_zoom]);

        console.log('~ life render x',step.life_speed,"zoom",step.life_zoom);
      };

      // TAKE DECISION
      if (t > (at - decideDelay) && !decideStarted){
        decideStarted = true;
        console.log(at);
        console.log('~ decide !');
        
        jump = getJumpIn(step);
      };
      // APPLY DECISION
      if(t > at){
        clearInterval(inter);
        console.log('life in', jump);

        setTimeout(function(){
          
          console.log('~ top !');

          movieCurentStep++;
          
          $d.trigger("showLife");
          $pop_movie.pause();

        },jump*1000);
      };
    },movieWatchInteval);
  };
  function onLifeEnded(){
    var step = score[movieCurentStep],
        jump = getJumpOut(step),
        at   = getAt(step);

    console.log("~ cut",step.id,step.title,'(',step.type,')',"@", at);
    console.log("restarting life at", jump,'/',step.jump_max);

    $pop_movie.play(at + jump);

    $d.trigger("showMovie");

    if(movieCurentStep > score.length - 2){
      $d.trigger("last_sequence");
    }else{
      movieCurentStep++;
      setNextStep();
      $d.trigger("last_sequence");
    }
  };
  function emulateImageFormation(freq) {
    //image_formation emulator 
    setInterval(function(){
      //var newImageFormation = ((image_formation + 1)%100);
      var newImageFormation = Math.floor(Math.random() * 100) + 1;
      
      $d.trigger("image_formation", newImageFormation);
      //console.log("f="+image_formation);s
    }, freq*1000); 
  }

  function sleep(milliseconds){
    var start = new Date().getTime();
    for(var i = 0 ; i < 10000000 ; i++){
      if((new Date().getTime() - start) > milliseconds){
        break;
      };
    };
  };

  function onTimerWait(){
    var start = new Date().getTime();
    var diff, min, sec;
    var interval = setInterval(function(){

    diff = Math.round((delay*1000 - (new Date().getTime() - start))/1000);
      if(diff < 0){
        clearInterval(interval);
      } else{
        min = Math.floor(diff/60);
        if(min < 10){
          min = "0" + min;
        };
        sec = diff%60;
        if(sec < 10){
          sec = "0" + sec;
        };
        document.getElementById('timer').innerHTML = 'Immersion dans<br \>00:' + min + ':' + sec;
      };
    }, 800);
  };

  reset();

};
$(document).on('ready', init);