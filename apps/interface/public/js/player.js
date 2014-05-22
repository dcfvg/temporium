function init() {

  var serverBaseUrl = document.domain,
      socket = io.connect(serverBaseUrl),
      sessionId = '',

      $d = $(document),
      $movie = $("#movie"),
      $life  = $("#life"),
      //$pop_movie = Popcorn("#movie"),
      $pop_life = Popcorn("#life"),

      score = {},

      mov_w = 1280,
      mov_h = 720,

      mov_length = 20808; // in seconds x 10 

      lifeUrl  = "/video/live.mp4",
      movieUrl = "/video/test_6canaux.mov",

      movieGoesOn = false,
      movieCurentEvent = 2,
      t_margin = 3

      image_formation = 0;
      ;

    
  //////////////////////////////
  // On
  //////////////////////////////

  socket.on('connect', onSocketConnect);
  socket.on('oscMessage', onSocketOscMessage);
  socket.on('score', onSocketScore);

  $d
  .on( "seance_start"     , function(e, obj) {
    console.log("session start " + obj);
    showMovie();})
  .on( "life_reload"      , reloadLife)
  .on( "image_formation"  , onImageFormation)
  .on( "player_reset"     , reset())
  .on( "showMovie"        , showMovie)
  .on( "showLife"         , showLife)
  .on( "player_seekTo"    , function(e,obj){qtSeekTo(obj[1]);});
  
  $pop_life.on("ended"    , function() {
    $pop_movie.play();
    showMovie();});

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
    socket.emit('newUser', {id: sessionId, name: $('#name').val()});
  };
  function onSocketOscMessage(obj){
    console.log(obj[0]);
    $d.trigger(obj[0],[ obj[1] ]);
  };
  function onSocketScore(obj){

    score = obj;
    console.log(obj);
    // Popcorn.forEach(score, function(l) {
    //   start = (parseInt(l.at_min)*60+ parseInt(l.at_sec))/60;
    //   console.log("set-"+ l.type, " at " + start);

    //   //$pop_movie.cue( start, function(){
    //     console.log("#"+l.id+":"+l.type+" ("+l.title +" "+ l.jump +") ");
    //   });
    // });
  };
  function onImageFormation(e){
    if(!movieGoesOn && parseInt(obj[1]) > 15){
      movieGoesOn = true;
    }
  }
  
  function setNewCut(){

    var l = score[movieCurentEvent],
        at = 10,//getAt(l),
        ct = 0;

    var wait = setInterval(function(){
      ct = getQtCurrentTime();
      console.log('ct: '+ct);

      mov_progress = Math.round((ct/mov_length)*100);

      if(ct > at - 60) {
        console.log("refreshTimelaps")
        // socket.emit('refreshTimelaps');
      }
      if(ct > at - t_margin){ // decision

        var jump = randomRange(t_margin , l.jump); 
        console.log("decide ! jump in "+jump);
        console.log("move_progress" , mov_progress, "image_formation", image_formation);

        clearInterval(wait);


        setTimeout(function(){ 
          console.log("life !");
        }, jump*1000);
      }
    }, 500);


  }


  //////////////////////////////
  // Helpers
  //////////////////////////////

  function randomRange (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  function getAt(l){
    return (parseInt(l.at_min)*60+ parseInt(l.at_sec));
  }
  function sToQtTimecode(sTc){
    // second timecode to QuickTime timecode

    var hours = parseInt( sTc / 3600 ) % 24;
    var minutes = parseInt( sTc / 60 ) % 60;
    var seconds = sTc % 60; 

    return (hours < 10 ? "0" + hours : hours) + ":" 
      + (minutes  < 10 ? "0" + minutes : minutes) + ":" 
      + (seconds  < 10 ? "0" + seconds : seconds) + ":00"; // add image count
  };
  function showMovie(){
    $movie.removeClass("off");
    $life.addClass("off");
    //$pop_movie.play();
  };
  function showLife(){
    $life.removeClass("off");
    $movie.addClass("off");
    $pop_life.play();
  };
  function reloadLife(){
    // add reload argument to avoid cache
    $life.attr("src",lifeUrl + "?reload="+Math.round((new Date()).getTime() / 1000)).load();
  };
  function blackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  };
  function getScore(){socket.emit('getScore',true)
  ;};
  function reset(){
    console.log("reset player");

    blackScreen();
    getScore();
    //socket.emit('refreshTimelaps');
    createQt(movieUrl, "00:00:00:00", $movie);

    movieGoesOn = false;

    // seek to beginning 
    //$pop_movie.pause().currentTime(0);  
    //$pop_life.pause().currentTime(0);
  };

  // QT plugin implementation

  function initQtCallback(){
    console.log("Register Qt player Event");

    var obj = document.qtinstance1;
    obj.addEventListener('qt_error', onQtPlayerEvent, false);
    obj.addEventListener('qt_pause', onQtPlayerEvent, false);
    obj.addEventListener('qt_stalled', onQtPlayerEvent, false);
    obj.addEventListener('qt_ended', onQtPlayerEvent, false);
    obj.addEventListener('qt_begin', onQtPlayerEvent, false);
    obj.addEventListener('qt_validated', onQtPlayerEvent, false);
    obj.addEventListener('qt_canplay', onQtPlayerEvent, false);
    obj.addEventListener('qt_canplaythrough', onQtPlayerEvent, false);
  };
  function createQt(qtsrc, time, container, id){

    container.html(QT_GenerateOBJECTText(
      qtsrc, mov_w, mov_h, 'sff',
      'obj#id'  , 'qtinstance1',
      'emb#NAME', 'qtinstance1' ,
      'emb#id'  , 'qtinstance1' ,
      'scale' , 'tofit' , 'AUTOPLAY', 'true', 'CONTROLLER', 'false',
      'EnableJavaScript', 'True', 'postdomevents', 'True',
      'STARTTIME',time,
      'qtsrc', qtsrc));

      initQtCallback();
  };
  function getQtCurrentTime(){
    return document.qtinstance1.GetTime();
  }
  function qtSeekTo(t){
    console.log("seek -> "+ t);
    createQt(movieUrl, sToQtTimecode(t), $movie);
  };
  function onQtPlayerEvent(ev){
    console.log("Event! " + ev.type);         
  };

  reset();
  setTimeout(function() {
    setNewCut();
  }, 250);


};
$(document).on('ready', init);