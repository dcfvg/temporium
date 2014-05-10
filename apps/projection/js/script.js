$(function() {
  
	/* 
	// http://popcornjs.org/popcorn-docs/getting-started/
	// http://jsfiddle.net/popcornjs/G3Csf/
	// https://www.npmjs.org/package/osc.io
	
	*/

	var $movie = $("#movie"),
  		$life  = $("#life"),
 			$pop_movie = Popcorn("#movie"),
			$pop_life = Popcorn("#movie");
	
	// functions
	
	function showMovie(){
		$movie.removeClass("off");
		$life.addClass("off");
	}
	function showLife(){
		$life.removeClass("off");
		$movie.addClass("off");
	}
	function blackScreen(){
		$life.addClass("off");
		$movie.addClass("off");
	}
	function reset (){
		blackScreen();
		
		// seek to beginning 
		$pop_movie.currentTime(0);	
		$pop_life.currentTime(0)
		
	}
	function reloadLife(){
		// add reload argument to avoid cache
		$life.attr("src","assets/life.mp4?reload="+Math.round((new Date()).getTime() / 1000)).load();
	}
	function getLifeState(){
		// grab get value from csv file ± every minute
		// event OSC 
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
  socket.on('message', function(obj) {
      console.log(obj);

			switch (obj[0]) {
			case "/seance_start":
				
				showMovie();
				$pop_movie.play();
			
			break;
			case "/life_reload":
				reloadLife();
			break;
			case "AHAHA":
			    day = "Monday";
			break;
				
			default:
				text ="hein ?";
			}
  });

	// cue manager
		
	$pop_movie.cue( 2, function() {
	    this.currentTime( 10.5 ).play();
	});
	$pop_movie.cue( 12, function() {
			$pop_life.play();
			showLife();
	});
	$pop_movie.cue( 20, function() {
			console.log( "from:"+this.currentTime());
			showMovie();
	});
	
	// player event 
	
	$movie.on("ended", function() {
			console.log("seance_end ! ");
			blackScreen();
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

});