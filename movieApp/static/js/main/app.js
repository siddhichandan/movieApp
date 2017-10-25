if (typeof jQuery === "undefined") {
  throw new Error("AdminLTE requires jQuery");
}

(function($, document, window){
	
	$(document).ready(function(){

		console.log("Fetching movies");
		// Cloning main navigation for mobile menu
		$(".mobile-navigation").append($(".main-navigation .menu").clone());

		// Mobile menu toggle 
		$(".menu-toggle").click(function(){
			$(".mobile-navigation").slideToggle();
		});
		$(".search-form button").click(function(){
			$(this).toggleClass("active");
			var $parent = $(this).parent(".search-form");

			$parent.find("input").toggleClass("active").focus();
		});


		$(".slider").flexslider({
			controlNav: false,
			prevText:'<i class="fa fa-chevron-left"></i>',
			nextText:'<i class="fa fa-chevron-right"></i>',
		});
		if( $(".map").length ) {
			$('.map').gmap3({
				map: {
					options: {
						maxZoom: 14 
					}  
				},
				marker:{
					address: "40 Sibley St, Detroit",
				}
			},
			"autofit" );
	    	
	    }
	    console.log("Fetching movies");
	    getFeaturedMovies();
	});

	$(window).load(function(){

	});

})(jQuery, document, window);

$(function () {
  //custom search
 console.log("In here");
 alert("Hey");
});

function getFeaturedMovies(){
	console.log("In get getFeaturedMovies");
	$.ajax({
    method: "GET",
    url: "/email/action="+action,
    traditional: true,
    async: false,
    complete: function(data){
      console.log("Completed")
      console.log(data)
    }
  })
  .done(function( data ) {
    print(data);
    var text = data.response.body;
    var url = data.response.url;
    submitMailTo(url, text);
  })
  .fail(function(jqXHR){
    if(jqXHR.status==500 || jqXHR.status==0){
      var message = 'Oops! Something went wrong.</h3><p>We will work on fixing that right away.Meanwhile, you may try using the other search queries.';
      print(message);
    }
  });

}