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
  console.log('oi');
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
           }
       );
   });

   socket.on('message', function(obj) {
       console.log(obj);
   });

	// cue manager
		
	$pop_movie.cue( 2, function() {
			console.log( "from:"+this.currentTime() );
	    this.currentTime( 10.5 ).play();
			console.log( "to:"+this.currentTime() );
	});
	$pop_movie.cue( 12, function() {
			console.log( "from:"+this.currentTime());
			showLife();
	});
	
	$pop_movie.cue( 20, function() {
			console.log( "from:"+this.currentTime());
			showMovie();
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

	var server = io.connect('http://localhost/osc/servers/8000'),
	  client = io.connect('http://localhost/osc/clients/8000');

	server.on('message', function(message) {
	  console.log(message);
	});

	setInterval(function() {
	  client.emit('message', ['/osc/test', 200]);
	}, 500);

});