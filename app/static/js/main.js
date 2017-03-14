var current_search = "";

$(document).ready(function(){
    $("#searchButton").click(function(){
    	var search_terms = $("#searchForm").serializeArray()[1]["value"];	
    	$("#results").html('');
    	load_posts(search_terms);
    	current_search = search_terms;
    });
});

function load_posts(terms) {
	$("#loadMore").remove();
   	var url = "/results/" + terms;
	$('#results').append('<li id="loadMarker" class="list-group-item">LOADING</li>');
	$("#results").load(url, searchCallback);
};

function searchCallback(result){
	// remove loading message

	$("#loadMore").click(function(){
		
    	load_posts(current_search);
    });

    $("#loadMore").waypoint(function(){
	if (current_search !== "" && !$("#endMarker").length) {
		load_posts(current_search);
	}
}, { offset: 100 });
};
