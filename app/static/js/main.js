$(document).ready(function(){
    $("#searchForm").submit(function(){
        sendSearch($("#search").val());
    });
    $("#searchButton").click(function(){
        sendSearch($("#search").val());
    });
    $("#savedSearchButton").click(function(){
        sendSearch($("#savedSearchTerms").text());
    });
});

function sendSearch(search_terms){
    // remove old warning box
    $(".alert").remove();

    // empty the current results
    $("#results").html('');

    // get search terms from form and request the results
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
	$('#results').append('<li id="loadMarker" class="list-group-item">LOADING (this may take a minute)</li>');

    // request results and add them to the DOM
	$("#results").load(url, searchCallback);
}

function searchCallback(result){
	// remove loading message
    $("#loadMarker").remove();
}
