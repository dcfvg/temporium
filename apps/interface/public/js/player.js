function init() {

  var serverBaseUrl = document.domain,
      socket = io.connect(serverBaseUrl),
      sessionId = '',

      $d = $(document),
      $movie = $("#movie"),
      $life  = $("#life"),
      //$pop_movie = Popcorn("#movie"),
      $pop_life = Popcorn("#life"),

      score,
      mov_w = 1280,
      mov_h = 720,

      lifeUrl  = "/video/live.mp4",
      movieUrl = "/video/test_6canaux.mov"

      ;
    
  //////////////////////////////
  // On
  //////////////////////////////

  socket.on('connect', onSocketConnect);
  socket.on('oscMessage', onSocketOscMessage);
  socket.on('score', onSocketScore);

  $d
  .on( "seance_start", function(e, obj) {
    console.log("session start " + obj);
    showMovie();
  })
  .on( "life_reload", reloadLife)
  .on( "image_formation", function(e, obj){
    if(!started && parseInt(obj[1]) > 15){
      started = true;
      showMovie();
    }
  })
  .on( "player_reset", reset())
  .on( "showMovie", showMovie)
  .on( "showLife", showLife)
  .on( "player_seekTo", function(e,obj){
    qtSeekTo(Math.floor((Math.random() * 30) + 1));
  });
  $pop_life.on("ended", function() {
    $pop_movie.play();
    showMovie();
  });

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
    score = obj; // un

    // Popcorn.forEach(score, function(l) {
    //   start = (parseInt(l.at_min)*60+ parseInt(l.at_sec))/60;
    //   console.log("set-"+ l.type, " at " + start);

    //   //$pop_movie.cue( start, function(){
    //     console.log("#"+l.id+":"+l.type+" ("+l.title +" "+ l.jump +") ");
    //   });
    // });
  };
  
  //////////////////////////////
  // Helpers
  //////////////////////////////

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
    $life.attr("src","life.mp4?reload="+Math.round((new Date()).getTime() / 1000)).load();
  };
  function blackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  };
  function getScore(){
    socket.emit('getScore',true);
  };
  function reset(){
    console.log("reset player");
    blackScreen();
    getScore();
    //socket.emit('refreshTimelaps');
    addQtPlayer(movieUrl, "00:00:04:00", $movie);

    // seek to beginning 
    //$pop_movie.pause().currentTime(0);  
    //$pop_life.pause().currentTime(0);
  };

  // QT plugin implementation

  function initQtPlayerCallback(){
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
  function addQtPlayer(qtsrc, time, container, id){

    container.html(QT_GenerateOBJECTText(
      qtsrc, mov_w, mov_h, 'sff',
      'obj#id'  , 'qtinstance1',
      'emb#NAME', 'qtinstance1' ,
      'emb#id'  , 'qtinstance1' ,
      'scale' , 'tofit' , 'AUTOPLAY', 'false', 'CONTROLLER', 'false',
      'EnableJavaScript', 'True', 'postdomevents', 'True',
      'STARTTIME',time,
      'qtsrc', qtsrc));

      initQtPlayerCallback();
  }
  function qtSeekTo(t){
    console.log("seek -> "+ t);
    addQtPlayer(movieUrl, "00:00:"+t+":00", $movie);
  }
  function onQtPlayerEvent(ev){
    console.log("Event! " + ev.type);         
  };

  reset();
};
$(document).on('ready', init);