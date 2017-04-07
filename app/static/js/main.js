$(document).ready(function(){
    $("#searchButton").click(submitSearch);
});

function submitSearch(){
    // remove old warning box
    $(".alert").remove();

    // empty the current results
    $("#results").html('');

    // get search terms from form and request the results
    var search_terms = $("#searchForm").serializeArray()[1].value;
    load_posts(search_terms);
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
