var clearErrorMsg = function() {
	$(".error").empty();
}

var printError = function(msg) {
	$temp = "<p>" + msg + "</p>"
	$(".error").append($temp);
}

var checkInputField = function(event) {
	clearErrorMsg();
	/* var patt1 = new RegExp("") */
	/* if (!$("#id_username").val().match(patt1)) printError();  */
	if ($("#id_username").val() == ""){ 
		event.preventDefault();
		printError("请输入用户名~!");
	}
	if ($("#id_password").val() == ""){ 
		event.preventDefault();
		printError("请输入密码~!");
	}
}

var login = function(event) {
	$("form").submit(checkInputField);
}

window.onload = login;
