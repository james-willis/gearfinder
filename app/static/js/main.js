var pg_num = 1;
var current_search = "";

$(document).ready(function(){
	var search_terms = $("#searchForm").serializeArray()[1]["value"];
    $("#searchButton").click(function(){
    	pg_num = 1;
    	var url = "http://localhost:5000/results/" + search_terms + "/" + pg_num + "/";
    	$("#results").html("");
    	$.getJSON(url, searchCallback);
    	pg_num += 1;
    	current_search = search_terms;
    });

    $("#footer").waypoint(function(){
    	if (current_search !== "") {
	   		var url = "http://localhost:5000/results/" + current_search + "/" + pg_num + "/";
			$.getJSON(url, searchCallback);
			pg_num += 1;
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

function getDocHeight() {
    var D = document;
    return Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    );
}
