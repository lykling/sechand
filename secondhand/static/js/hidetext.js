
function longtext(){
	var title_len = 13;
	var descrip_len = 29;
	var titles = document.getElementsByName("Title");
	var descrips = document.getElementsByName("Description")
		var s = null;
	var p = null;
	var n = null;
	var i = 0;
	for (i = 0; i < titles.length; i ++) {
		s = titles[i].innerHTML;
		p = document.createElement("span");
		n = document.createElement("font");
		p.innerHTML = s.substring(0, title_len);
		n.innerHTML = s.length > title_len ? "...":"";
		titles[i].innerHTML = ""
			titles[i].appendChild(p);
		titles[i].appendChild(n);
	}
	for (i = 0; i < descrips.length; i ++) {
		s = descrips[i].innerHTML;
		p = document.createElement("span");
		n = document.createElement("font");
		p.innerHTML = s.substring(0, descrip_len);
		n.innerHTML = s.length > descrip_len ? "...":"";
		descrips[i].innerHTML = ""
			descrips[i].appendChild(p);
		descrips[i].appendChild(n);
	}
}
function handler() {
	longtext();
}
$(document).ready(handler);
