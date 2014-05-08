$(function() {
  
	console.log("ok");
		
	var $movie = $("#movie"),
  		$life  = $("#life");

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
	
	// http://popcornjs.org/popcorn-docs/getting-started/
	// http://jsfiddle.net/popcornjs/G3Csf/
	
	$("#movie")
		.bind("timeupdate", function() {
	   //console.log("Current time is " + this.currentTime);
		if(Math.floor(this.currentTime) == 3) console.log("ah!");
		})
	.bind("ended", function() {
		   alert("I'm done!");
		});
	
	$(document).keypress(function( event ){
    console.log(event.which);

		//m -> movie
    if ( event.which == 108 ) showMovie(); 
    
		//l -> life
    if ( event.which == 109 ) showLife();
		
		//r -> refreshlife
    if ( event.which == 114 ) reloadLife();
  });


});