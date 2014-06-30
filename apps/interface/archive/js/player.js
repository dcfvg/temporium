function init() {

  //////////////////////////////
  // vars
  //////////////////////////////

  var serverBaseUrl = "http://localhost:8080",
      socket = io.connect(serverBaseUrl),
      sessionId = '',
      $d = $(document)
      ;

  var $movie            = $("#movie"),                  // container
      movieUrl          = "/video/immersion.mov",       // video file url
      movieWidth        = 1920, movieHeight = 1036,     // size to display
      movieGoesOn       = false,                        // 
      movieCurentStep   = 0,                            // current event step
      movieWatchInteval = 500,                          // timecode events refresh frequency
      movieTimeScale    = 25,                           // qt property
      movieDuration     = 1935,                         // duration of the movie
      movieStartMargin  = 44,
      movieVolume       = 255
      ;

  var $life             = $("#life"),
      lifeUrl           = "/video/live.mp4",
      $pop_life         = Popcorn("#life")
      ;

  var image_formation = 50,
      formationStartLevel = 20,
      compileDelay = 120,
      decideDelay = 2
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
    .on( "lifeRefreshMovie" , onReloadLife)
    .on( "image_formation"  , onImageFormation)
    .on( "player_reset"     , reset)
    .on( "showMovie"        , onShowMovie)
    .on( "showLife"         , onShowLife)
    .on( "projectionStart"  , onProjectionStart)
    .on( "qtSeekTo"         , onQtSeekTo) 
  ;
  
  $pop_life.on("ended",onLifeEnded);

  // dev shortcuts
  $d.keypress(function( event ){
    //console.log(event.which);
    if ( event.which == 109 ) $d.trigger("showMovie");  // m
    if ( event.which == 108 ) $d.trigger("showLife");   // l
    if ( event.which == 114 ) $d.trigger("reloadLife"); // r
    if ( event.which == 104 ) { // h
      var time  = (getQtCurrentTime()+30) * movieTimeScale;
      document.qtF.SetTime(time);
      console.log("jump +30s -> "+time/movieTimeScale);
    };
    if ( event.which == 106 ) { // j
      var time  = (getQtCurrentTime()+10) * movieTimeScale;
      document.qtF.SetTime(time);
      console.log("jump +10s -> "+time/movieTimeScale);
    };

    if ( event.which == 107 ) { console.log("t :",getQtCurrentTime());}// k

    if ( event.which == 103 ) $d.trigger("projectionStart"); //g
  });

  //////////////////////////////
  // HANDLERS 
  //////////////////////////////

  // messages events
  function onSocketConnect() {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);
    //socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  function onSocketOscMessage(obj){
    console.log(obj);
    $d.trigger(obj[0],[ obj[1] ]);
  };
  function onSocketScore(obj){
    score = obj;
    console.log(obj);
  };

  // seance == top vivant
  function onSeanceStart(){
    console.log("# seance seance_start !");
    $d.trigger("projectionStart");

    socket.emit('captureInit',true);
  };
  // projection == film
  function onProjectionStart(){
    
    console.log("# projection !");
 
    document.qtF.Play();
    $d.trigger("showMovie");
    
    movieGoesOn = true;

    movieCurentStep = 0;
    setNextStep();
    setQtVolume(movieVolume);
  }

  // player events
  function onImageFormation(e, obj){

    image_formation = parseInt(obj);
    console.log('image_formation updt',image_formation);

    if(!movieGoesOn && parseInt(obj) > formationStartLevel){
      $d.trigger("projectionStart");
    };
  };
  function onReloadLife(){
    // add reload argument to avoid cache
    if($life.hasClass("off")) $life.attr("src",lifeUrl + "?reload="+Math.round((new Date()).getTime() / 1000)).load();
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
  };
  function onShowLife(){
    $pop_life.play();
    $life.removeClass("off");
    $movie.addClass("off");
  };
  function onBlackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  };

  //////////////////////////////
  // Helpers
  //////////////////////////////

  function getScore(){socket.emit('getScore',true);
  };
  function getAt(l){
    return (parseInt(l.at_min)*60 + parseInt(l.at_sec) + movieStartMargin); 
  };
  function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  // QT plugin manipulation
  function createQt(qtsrc, container, name){
    container.html(QT_GenerateOBJECTText(
      qtsrc, movieWidth, movieHeight, 'sff',
      'obj#id'  , name,
      'emb#NAME', name,
      'emb#id'  , name,
      'scale' , 'tofit' , 'AUTOPLAY', 'false', 'CONTROLLER', 'false',
      'EnableJavaScript', 'True', 'postdomevents', 'True',
      'STARTTIME',"00:00:00:00",
      'qtsrc', qtsrc));

    initQtCallback();
  };
  function initQtCallback(){
    console.log("Register Qt player Event");

    var obj = document.qtF;
    obj.addEventListener('qt_error'         , onQtPlayerEvent, false);
    obj.addEventListener('qt_pause'         , onQtPlayerEvent, false);
    obj.addEventListener('qt_stalled'       , onQtPlayerEvent, false);
    obj.addEventListener('qt_ended'         , onQtEnded, false);
    obj.addEventListener('qt_begin'         , onQtPlayerEvent, false);
    obj.addEventListener('qt_validated'     , onQtPlayerEvent, false);
    obj.addEventListener('qt_canplay'       , onQtPlayerEvent, false);
    obj.addEventListener('qt_canplaythrough', onQtCanPlayThrough, false);
  };
  function sToQtTimecode(sTc){
    // second timecode to QuickTime timecode

    var hours = parseInt( sTc / 3600 ) % 24;
    var minutes = parseInt( sTc / 60 ) % 60;
    var seconds = sTc % 60; 

    return (hours < 10 ? "0" + hours : hours) + ":" 
      + (minutes  < 10 ? "0" + minutes : minutes) + ":" 
      + (seconds  < 10 ? "0" + seconds : seconds) + ":00"; // add image count
  };
  function setQtVolume(v){
    document.qtF.SetVolume(v);
  };
  function getQtCurrentTime(){
    return Math.round(document.qtF.GetTime()/movieTimeScale * 100)/100;
  };
  function onQtSeekTo(e, obj){
    console.log("seek -> "+ obj);
    // createQt(movieUrl, sToQtTimecode(t), $movie); // brute force
    document.qtF.SetTime(parseInt(obj));
  };
  function onQtPlayerEvent(ev){
    console.log("QtEvent :: " + ev.type);    
  };
  function onQtCanPlayThrough(){
    $("#wait").addClass('off');

    movieTimeScale = document.qtF.GetTimeScale();
    movieDuration  = document.qtF.GetDuration() / movieTimeScale;

    //emulateImageFormation(60);

    console.log("movie is ready !", movieTimeScale, movieDuration);
  };
  function onQtEnded(){
    io.sockets.emit("message", "seance_end");
    
    socket.on("captureStop", onCaptureStop);
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

    createQt(movieUrl, $movie, "qtF");
    movieGoesOn = false;

    // seek to beginning 

    document.qtF.Stop(0);
    document.qtF.SetTime(0);
  
    $pop_life.pause().currentTime(0);

    //$pop_life.pause().currentTime(0);
  };
  function getJump(step){
    var jump_max = step.jump_max;
    var movieProgress  = Math.round((getQtCurrentTime()/movieDuration)*100);
    var lifeProgress = image_formation; //Math.round((image_formation/255)*100);
    var jump = (jump_max/2)-(((lifeProgress - movieProgress)/100)*jump_max);

    if(jump > jump_max) jump = jump_max; // to FIX 

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

      t = getQtCurrentTime();

      // TIMELAPS COMPILATION
      if(t > (at - compileDelay) && !renderStarted){
        renderStarted = true;
        socket.emit('refreshTimelaps',[step.life_speed, step.life_zoom]);

        console.log('~ life render x',step.life_speed,"zoom",step.life_zoom);
      };

      // TAKE DECISION
      if (t > (at - decideDelay) && !decideStarted){
        decideStarted = true;
        console.log('~ decide !');
        
        jump = getJump(step);
      };
      // APPLY DECISION
      if(t > at){
        clearInterval(inter);
        console.log('life in', jump);

        setTimeout(function(){
          
          console.log('~ top !');

          movieCurentStep++;

          $d.trigger("showLife"); // show life 
          document.qtF.Stop();   // stop movie

        },jump*1000);
      };
    },movieWatchInteval);
  };
  function onLifeEnded(){
    var step = score[movieCurentStep],
        jump = getJump(step),
        at   = getAt(step);

    console.log("~ cut",step.id,step.title,'(',step.type,')',"@", at);
    console.log("restarting life at", jump,'/',step.jump_max);

    document.qtF.SetTime((at + jump) * movieTimeScale);
    document.qtF.Play();

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

  reset();

};
$(document).on('ready', init);