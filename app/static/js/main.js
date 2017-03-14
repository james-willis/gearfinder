var current_search = "";

$(document).ready(function(){
	var search_terms = $("#searchForm").serializeArray()[1]["value"];
    $("#searchButton").click(function(){
    	pg_num = 1;
    	var url = "/results/" + search_terms;
    	$("#results").html("");
    	$.getJSON(url, searchCallback);
    	pg_num += 1;
    	current_search = search_terms;
    });

    $(".footer").waypoint(function(){
    	if (current_search !== "") {
	   		var url = "/results/" + current_search;
			$.getJSON(url, searchCallback);
		}
	}, { offset: 100 });
});

function searchCallback(result){
	$.each(result, function(i, field){
        $("#results").append(makeResultHtml(i, field));
    });
};

function makeResultHtml(title, link) {
return '<a href="' + link +'"' + 'target="_blank"><li class="list-group-item">' + title + 
"</li></a>";
};

