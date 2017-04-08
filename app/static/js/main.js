$(document).ready(function(){
    $("#searchButton").click(submitSearch);
});

function submitSearch(){
    // remove old warning box
    $(".alert").remove();

    // empty the current results
    $("#results").html('');

    // get search terms from form and request the results
    var search_terms = $("#search").val();
    if (search_terms) {
        load_posts(search_terms);
    }
    else {
        $("#flashes").append('<div class="alert alert-danger", role="alert">Search must not be empty</div>');
    }
}

function load_posts(terms) {
    // build url and add loading message
   	var url = "/results/" + terms;
	$('#results').append('<li id="loadMarker" class="list-group-item">LOADING</li>');

    // request results and add them to the DOM
	$("#results").load(url, searchCallback);
}

function searchCallback(result){
	// remove loading message
    $("#loadMarker").remove();
}
