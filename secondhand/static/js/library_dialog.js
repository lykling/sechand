var productid;
function getform(name, method){
	var url = "/product/" + productid + "/"
	if (method == "post") {
		var ask = $("#id_ask").val();
		var student_num = $("#id_student_num").val();
		var time_lent = $("#id_time_lent").val();
		var quantity = $("#id_quantity").val();
		var productname = $("#id_name").val();
		var author = $("#id_author").val();
		var translator = $("#id_translator").val();
		var press = $("#id_press").val();
		var isbn = $("#id_isbn").val();
		var comment = $("#id_comment").val();
		var num_in_library = $("#id_num_in_library").val()
		$.post(url, {'form_name':name, 'ask':ask, 'name':productname, 'product_id':productid, 'author':author, 'translator':translator, 'press':press, 'isbn':isbn, 'student_num':student_num, 'time_lent':time_lent, 'quantity':quantity, 'num_in_library':num_in_library, 'comment':comment}, function(data) {
				if (name == "lend") {
				$("#lendform").html(data);
				$("#lendform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "renew") {
				$("#renewform").html(data);
				$("#renewform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "delete") {
				$("#deleteform").html(data);
				$("#deleteform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "reserve") {
				$("#reserveform").html(data);
				$("#reserveform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "return") {
				$("#returnform").html(data);
				$("#returnform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "modify") {
				$("#modifyform").html(data);
				$("#modifyform").dialog("open");
				refreshPage(location.href);
				}
				else if (name == "comment") {
				$("#commentform").html(data);
				$("#commentform").dialog("open");
				refreshPage(location.href);
				}
		})
	}
	else if (method == "get") {
		//$.get("", {$("#.shortcut").name:$("#.shortcut").value}, function(data){
		$.get(url, {'form_name':name, 'productid':productid}, function(data){
				//$.get("", {"/renew/":"2"}, function(data){
				//$("#dialog_form").html(data['form']);
				//$("#dialog_form").html(data);
			if (name == "lend") {
				$("#lendform").html(data);
				$("#lendform").dialog("open");
			}
			else if (name == "renew") {
				$("#renewform").html(data);
				$("#renewform").dialog("open");
			}
			else if (name == "delete") {
				$("#deleteform").html(data);
				$("#deleteform").dialog("open");
			}
			else if (name == "reserve") {
				$("#reserveform").html(data);
				$("#reserveform").dialog("open");
			}
			else if (name == "return") {
				$("#returnform").html(data);
				$("#returnform").dialog("open");
			}
			else if (name == "modify") {
				$("#modifyform").html(data);
				$("#modifyform").dialog("open");
			}
			else if (name == "comment") {
				$("#commentform").html(data);
				$("#commentform").dialog("open");
			}
			//				$("#lendform").parent().appendTo("#aaaa");
		});	
		}
	};
	$(document).ready(function(){
			$(".reserve").click( function() {productid = $(this).attr('name'); getform("reserve", "get")});
			$(".return").click( function() {productid = $(this).attr('name'); getform("return", "get")});
			$(".renew").click( function() {productid = $(this).attr('name'); getform("renew", "get")});
			$(".lend").click( function() {productid = $(this).attr('name'); getform("lend", "get")});
			$(".del").click( function() {productid = $(this).attr('name'); getform("delete", "get")});
			$(".modify").click( function() {productid = $(this).attr('name'); getform("modify", "get")});
			$(".comment").click( function() {productid = $(this).attr('name'); getform("comment", "get")});
			//$("#id_submit_lend").click( function() {getform("lend", "get")});
			$("#lendform").dialog({
				autoOpen: false,	
				//height:250,
				//width:350,
				modal:true,
				resizable:false,
				/* position:"center", */
				buttons:{
					"借阅":function() {
						getform('lend', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#lendform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#renewform").dialog({
				autoOpen: false,	
				//height:400,
				//width:450,
				modal:true,
				resizable:false,
				buttons:{
					"续借":function() {
						getform('renew', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#renewform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#deleteform").dialog({
				autoOpen: false,	
				//height:400,
				//width:450,
				modal:true,
				resizable:false,
				buttons:{
					"删除":function() {
						getform('delete', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#deleteform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#reserveform").dialog({
				autoOpen: false,	
				//height:400,
				//width:450,
				modal:true,
				resizable:false,
				buttons:{
					"预定":function() {
						getform('reserve', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#reserveform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#returnform").dialog({
				autoOpen: false,	
				//height:400,
				//width:450,
				modal:true,
				resizable:false,
				buttons:{
					"归还":function() {
						getform('return', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#returnform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#modifyform").dialog({
				autoOpen: false,	
				//height:400,
				//width:450,
				modal:true,
				resizable:false,
				buttons:{
					"保存":function() {
						getform('modify', 'post')
					},
				"取消":function() {
					$(this).dialog("close");
				}
				},
				close: function() {
					$("#modifyform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
			$("#commentform").dialog({
				autoOpen: false,	
				//height:400,
				width: '700px',
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
					$("#commentform").empty()
				//allFields.val("").removeClass("ui-state-error");
				}
			});
	});

var refreshPage = function(url) {
	var flag = $("#flag").val();
	if (flag == 1) {
		setTimeout("window.location.assign('" + url + "')", 500);
	}
}
