var checkInputField = function(event) {
	/* var patt1 = new RegExp("") */
	/* if (!$("#id_username").val().match(patt1)) printError();  */

	if ($("#search_text").val() == ""){ 
		
		event.preventDefault();
	}
}

var onLoad = function(event) {
	$("#search").submit(checkInputField);
}

window.onload = onLoad;
