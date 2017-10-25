(function($, document, window){
	
	$(document).ready(function(){

		console.log("Howdy 2");

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
	    //console.log(fetching the movies);
	    getFeaturedMovies()
	});

	$(window).load(function(){

	});

})(jQuery, document, window);

function getFeaturedMovies(){
	console.log("In get getFeaturedMovies");
	$.ajax({
    method: "GET",
    url: "/movies/10",
  })
  .done(function( data ) {
    console.log(data);
    /*var jsonobj = $.parseJSON(data);
    console.log(jsonobj);
    if(jsonobj["status"] == "success"){
    	response = jsonobj["response"];
    	$('#featuredList').append(response["html"]);

    }*/
    $('#latest-movie').html(data);
    
  })
  .fail(function(jqXHR){
    if(jqXHR.status==500 || jqXHR.status==0){
      var message = 'Oops! Something went wrong.</h3><p>We will work on fixing that right away.Meanwhile, you may try using the other search queries.';
      console.log(message);
    }
  });
}

function openSearchResult(){

	var search = ""
	var search = $('#search').val()
	console.log("Value is" + search)
	if(search == ""){
		return
	}
	open_url = $('#search').data('search_url');
	open_url = open_url.replace('query', search);
	window.open(open_url);
}