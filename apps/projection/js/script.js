$(function() {
  
	/* 
	// http://popcornjs.org/popcorn-docs/getting-started/
	// http://jsfiddle.net/popcornjs/G3Csf/
	// https://www.npmjs.org/package/osc.io
	
	*/

	var $movie = $("#movie"),
  		$life  = $("#life");
			
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
		$life.attr("src","assets/life.mp4?reload="+Math.round((new Date()).getTime() / 1000)).load();
	}
	function getLifeState(){
		// grab get value from csv file ± every minute
	}
	
	// cue manager
	
	var $pop_mov = Popcorn("#movie");
	$pop_mov.cue( 2, function() {
			console.log( "from:"+this.currentTime() );
	    this.currentTime( 10.5 ).play();
			console.log( "to:"+this.currentTime() );
	});
	// shortcuts
	$(document).keypress(function( event ){
    //console.log(event.which);

		//m -> movie
    if ( event.which == 108 ) showMovie(); 
    
		//l -> life
    if ( event.which == 109 ) showLife();
		
		//r -> refreshlife
    if ( event.which == 114 ) reloadLife();
		
		//s 
		if ( event.which == 115 ) {
				$pop_mov.currentTime( 1 ).play();
		};
		
	
  });

});