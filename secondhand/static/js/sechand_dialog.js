var user_id;
var product_id;
function getform(name, method) {
	var url = '/profile/' + user_id + '/'
		if (method == "get") {
			$.get(url, {'form_name':name, 'uid':user_id}, function(data) {
				if (name == 'comment') {
					$("#commentuserform").html(data);
					$("#commentuserform").dialog("open");
				}
			});
		}
		else if (method == "post") {
			var content = $("#id_comment").val();
			$.post(url, {'form_name':name, 'comment':content}, function(data) {
				if (name == "comment") {
					$("#commentuserform").html(data);
					$("#commentuserform").dialog("open");
					refreshPage(location.href);
				}
			});
		}
}
var refreshPage = function(url) {
	var flag = $("#flag").val();
	if (flag == 1) {
		setTimeout("window.location.assign('" + url + "')", 500);
	}
}
function handler() {
	$("#comment").click(function() {user_id=$(this).attr('name'); getform('comment', 'get')});
	$("#commentuserform").dialog({
		autoOpen: false,
		modal:true,
		resizable:false,
		buttons:{
			"评论":function() {
				getform('comment', 'post')
			},
		"取消":function() {
			$(this).dialog("close");
		}
		},
		close: function() {
			$("#commenuserform").empty()
		}
	});
}
$(document).ready(handler);
