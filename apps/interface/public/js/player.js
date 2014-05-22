function init() {

  //////////////////////////////
  // vars
  //////////////////////////////
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
      t_margin = 3,

      image_formation = 0,
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
  
  $pop_life.on("ended", function() {
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
    //console.log(obj[0]);
    $d.trigger(obj[0],[ obj[1] ]);
  };
  function onSocketScore(obj){

    score = obj;
    console.log(obj);
    // Popcorn.forEach(score, function(l) {
    //   start = (parseInt(l.at_min)*60+ parseInt(l.at_sec))/60;
    //   console.log("set-"+ l.type, " at " + start);

    //   //$pop_movie.cue( start, function(){
    //     console.log("#"+l.id+":"+l.type+" ("+l.title +" "+ l.jump_max +") ");
    //   });
    // });
  };
  function onImageFormation(e, obj){
    if(!movieGoesOn && parseInt(obj) > formationStartLevel){
      onSeanceStart();
    };
  };
  function setNewCut(){

    var l = score[movieCurentEvent],
        at = 10,//getAt(l),
        ct = 0;

    var wait = setInterval(function(){
      ct = getQtCurrentTime();
      console.log('ct: '+ct);


      if(ct > at - 60) {
        console.log("refreshTimelaps")
        socket.emit('refreshTimelaps');
      }
      if(ct > at - t_margin){ // decision

        //var jump = randomRange(t_margin , l.jump_max); // dev value
        var jump = getJump(l, ct);
        console.log("decide ! jump in "+jump);

        getJump(l, ct)
        clearInterval(wait);

        setTimeout(function(){ 
          console.log("life !");
        }, jump*1000);
      }
    }, 500);
  };
  function onShowMovie(){
    $movie.removeClass("off");
    $life.addClass("off");
    //$pop_movie.play();
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
    movieGoesOn = true;
    document.qtF.Play();
    setNewCut();
    setQtVolume(0);
  };

  function blackScreen(){
    $life.addClass("off");
    $movie.addClass("off");
  };

  //////////////////////////////
  // Helpers
  //////////////////////////////
  function getJump(l, ct){
    var mov_progress  = Math.round((ct/mov_length)*100);
    var life_progress = Math.round((image_formation/255)*100);

    // milieu du plan on retire le différenciel entre le mov_progress et le life_progress
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
      qtsrc, mov_w, mov_h, 'sff',
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
    return document.qtF.GetTime();
  };
  function onQtSeekTo(e, obj){
    console.log("seek -> "+ obj);
    // createQt(movieUrl, sToQtTimecode(t), $movie); // brute force
    document.qtF.SetTime(parseInt(obj));
  };
  function onQtPlayerEvent(ev){
    console.log("Event! " + ev.type);    
  };
  function onQtCanPlay(){
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
    //$pop_movie.pause().currentTime(0);  
    //$pop_life.pause().currentTime(0);
  };

  reset();

  setInterval(function(){
    image_formation++;
    $d.trigger("image_formation", image_formation);
    console.log("f="+image_formation);
  }, 1000);
};
$(document).on('ready', init);