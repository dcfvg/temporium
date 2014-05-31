function init() {

  //////////////////////////////
  // vars
  //////////////////////////////

  var serverBaseUrl = document.domain,
      socket = io.connect(serverBaseUrl),
      sessionId = '',
      $d = $(document)
      ;

  var $movie = $("#movie"),
      movieUrl = "/video/test_6canaux.mov",
      movieWidth = 1280, movieHeight = 720,
      movieGoesOn = false,        
      movieCurentStep = 0,
      movieWatchInteval = 250,
      movieTimeScale = 0,
      movieDuration = 0
      ;

  var $life  = $("#life"),
      lifeUrl  = "/video/live.mp4",
      $pop_life = Popcorn("#life")
      ;

  var image_formation = 0,
      formationStartLevel = 5
      ;

  //////////////////////////////
  // On
  //////////////////////////////
  socket.on('connect', onSocketConnect);
  socket.on('oscMessage', onSocketOscMessage);
  socket.on('score', onSocketScore);

  $d // on
    .on( "seance_start"     , onSeanceStart)
    .on( "life_reload"      , onReloadLife)
    .on( "image_formation"  , onImageFormation)
    .on( "player_reset"     , reset)
    .on( "showMovie"        , onShowMovie)
    .on( "showLife"         , onShowLife)
    .on( "qtSeekTo"         , onQtSeekTo)
  ;
  
  $pop_life.on("ended",onLifeEnded);

  // dev shortcuts
  $d.keypress(function( event ){
    //console.log(event.which);
    if ( event.which == 109 ) $d.trigger("showMovie");  // m
    if ( event.which == 108 ) $d.trigger("showLife");   // l
    if ( event.which == 114 ) $d.trigger("reloadLife"); // r
  });

  //////////////////////////////
  // HANDLERS 
  //////////////////////////////
  function onSocketConnect() {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);
    //socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  function onSocketOscMessage(obj){
    //console.log(obj[0]);
    $d.trigger(obj[0],[ obj[1] ]);
  };
  function onSocketScore(obj){
    score = obj;
    console.log(obj);
  };
  function onImageFormation(e, obj){
    if(!movieGoesOn && parseInt(obj) > formationStartLevel){
      onSeanceStart();
    };
    console.log('image_formation',obj);
  };
  function setNextStep(){

    var step = score[movieCurentStep],
        at = getAt(step)/100,
        compileDelay = 4,
        decideDelay = 2,
        renderStarted = false,
        decideStarted = false
        ;

    console.log("waiting for step",step.id,step.title, "@", at);

    var inter = setInterval(function(){

      t = getQtCurrentTime();

      // TIMELAPS COMPILATION
      if(t > (at - compileDelay) && !renderStarted){
        renderStarted = true;
        console.log('start life render x',step.life_speed,"zoom",step.life_zoom);

        //socket.emit('refreshTimelaps',(step.life_speed,step.life_zoom));
      };

      // TAKE DECISION
      if (t > (at - decideDelay) && !decideStarted) {
        decideStarted = true;

        var jump = getJump(step, t);
        console.log("decide ! jump in "+jump);
      };
      // APPLY DECISION
      if(t > at){
        clearInterval(inter);
        setTimeout(function(){
          
          console.log('APPLY decision');

          movieCurentStep++;
          setNextStep();

          $d.trigger("showLife", image_formation);

          document.qtF.Stop();

        },jump);
      };

    },movieWatchInteval);
  }
  function onShowMovie(){
    $movie.removeClass("off");
    $life.addClass("off");
  };
  function onShowLife(){
    $life.removeClass("off");
    $movie.addClass("off");
    $pop_life.play();
  };
  function onReloadLife(){
    // add reload argument to avoid cache
    $life.attr("src",lifeUrl + "?reload="+Math.round((new Date()).getTime() / 1000)).load();
  };
  function onSeanceStart(){

    document.qtF.Play();
    $d.trigger("showMovie", image_formation);
    
    movieCurentStep = 0;
    setNextStep();
    
    setQtVolume(0);
  };
  function onLifeEnded(){
    $d.trigger("showMovie");
  };
  function blackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  };

  //////////////////////////////
  // Helpers
  //////////////////////////////
  function getJump(l, ct){
    /* 
    calcul du cut (plan in) ou du saut (plan out)
    1. différenciel entre le mov_progress et le life_progress
    2. le pourcentage obtenu est retiré du plan à couper à partir du centre de -50% à +50%
    */
    var mov_progress  = Math.round((ct/movieDuration)*100);
    var life_progress = Math.round((image_formation/255)*100);

    var jump = (l.jump_max/2)-(((life_progress - mov_progress)/100)*l.jump_max);

    console.log('jump = '+jump+'/'+l.jump_max+' (film :'+mov_progress+'% '+' life :'+life_progress+'%)');

    return jump;
  };
  function getScore(){socket.emit('getScore',true);
  };
  function getAt(l){
    return (parseInt(l.at_min)*60+ parseInt(l.at_sec));
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
    obj.addEventListener('qt_ended'         , onQtPlayerEvent, false);
    obj.addEventListener('qt_begin'         , onQtPlayerEvent, false);
    obj.addEventListener('qt_validated'     , onQtPlayerEvent, false);
    obj.addEventListener('qt_canplay'       , onQtCanPlay    , false);
    obj.addEventListener('qt_canplaythrough', onQtPlayerEvent, false);
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
  function onQtCanPlay(){
    movieTimeScale = document.qtF.GetTimeScale();
    movieDuration  = document.qtF.GetDuration();
    console.log("qtReady");
  };

  //////////////////////////////
  // actions
  //////////////////////////////

  function reset(){
    console.log("reset player");

    blackScreen();
    getScore();
    //socket.emit('refreshTimelaps');
    createQt(movieUrl, $movie, "qtF");

    movieGoesOn = false;

    // seek to beginning 
    //$pop_life.pause().currentTime(0);
  };

  /*
  image_formation emulator 

  setInterval(function(){
    image_formation++;
    $d.trigger("image_formation", image_formation);
    console.log("f="+image_formation);
  }, 1000);
  */

  reset();

};
$(document).on('ready', init);