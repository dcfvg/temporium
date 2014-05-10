$(function() {
  
	/* 
	// http://popcornjs.org/popcorn-docs/getting-started/
	// http://jsfiddle.net/popcornjs/G3Csf/
	// https://www.npmjs.org/package/osc.io
	
	*/

	var $movie = $("#movie"),
  		$life  = $("#life"),
 			$pop_movie = Popcorn("#movie"),
			$pop_life = Popcorn("#life"),
			started=false;
	
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
	function reset (){
		blackScreen();
		
		started=false;
		
		// seek to beginning 
		$pop_movie.pause().currentTime(0);	
		$pop_life.pause().currentTime(0)
		
	}

	// OSC 
	socket = io.connect('http://127.0.0.1', { port: 8081, rememberTransport: false});
	socket.on('connect', function() {
		// sends to socket.io server the host/port of oscServer
		// and oscClient
		socket.emit('config',
		{
			server: {
				port: 3333,
				host: '127.0.0.1'
			},
			client: {
				port: 3334,
				host: '127.0.0.1'
			}
		});
	});
  socket.on('message', function(obj){
      console.log(obj);

			switch (obj[0]) {
				case "/seance_start":
					console.log("session start");
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
				
				default:
					text ="hein ?";
			};
  });

	// cue manager
	
	// 1er plan image vivante
	$pop_movie.cue( 4, function() {
			
			console.log("cut vivant 1");
			
			$pop_life.currentTime( 35 );
			showLife();
			$pop_movie.currentTime( 120 ).pause();
			
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
				$pop_movie.currentTime( 1 ).play();
		};
		
	
  });

	// reset();
});