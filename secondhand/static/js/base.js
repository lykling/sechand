var Onload = function(){
	$("#search_log").css({"position":"fixed", "top":0, "right":0});
	$("#totop").css({"display":"none"});
	$(document).scroll(function(){
		if ($(document).scrollTop() > 0) {
		$("#totop").css({"display":"block"});
		}	
		else {
		$("#totop").css({"display":"none"});
		}
		})
	$("#search_text").autocomplete({
		source: "/auto_complete/",
		select: function (event, ui){
		$("#search_text").val(ui.item.value);
		$("#search").submit();
	}})

	$(document).tooltip({
		position: {my: "left top", at: "right top"},	
	});
	$("#search").submit(checkInputField);
}

var checkInputField = function(event) {
	/* var patt1 = new RegExp("") */
	/* if (!$("#id_username").val().match(patt1)) printError();  */
	if ($("#search_text").val() == ""){ 
		event.preventDefault();
	}
}

window.onload = Onload;
