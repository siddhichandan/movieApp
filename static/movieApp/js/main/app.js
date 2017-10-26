
(function($, document, window){
	
	$(document).ready(function(){

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
	    getFeaturedMovies()
	});

	$(window).load(function(){

	});

})(jQuery, document, window);

function getFeaturedMovies(){
	console.log("In get getFeaturedMovies");
	$.ajax({
    method: "GET",
    url: "/movies/8",
  })
  .done(function( data ) {
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

function openAddmovieModal(url){
	console.log("In openAddmovieModal")
	console.log(url)
	$.ajax({
    method: "GET",
    url: url,
  })
  .done(function( data ) {
    $('#modal-data').html(data);
  })
  .fail(function(jqXHR){
    if(jqXHR.status==500 || jqXHR.status==0){
      var message = 'Oops! Something went wrong.</h3><p>We will work on fixing that right away.Meanwhile, you may try using the other search queries.';
      console.log(message);
    }
  });
	$("#addMovieModel").modal('toggle');
	 
}

function closeMoviemodal(){
	$("#addMovieModel").modal('toggle');
}

function submitThisForm(e){
	e.disabled = true;
	console.log("submitThisForm")

	var url = $('#submitForm').data('url') // the script where you handle the form input.

    $.ajax({
           type: "POST",
           url: url,
           data: $("#addMovieForm").serialize(), // serializes the form's elements.
    }).done(function( data ) {
    	if(typeof data == "string"){
              data = $.parseJSON(data);
         }
        status = data["status"];
        if(status == "success"){
        	alert("Operation successfull");
        } else {
        	alert(data["response"]["message"]);
        }
    	e.disabled=false
  	}).fail(function(jqXHR){
    if(jqXHR.status==500 || jqXHR.status==0){
      var message = 'Oops! Something went wrong.</h3><p>We will work on fixing that right away.Meanwhile, you may try using the other search queries.';
      console.log(message);
    }
  });

}