function get_options(id){
	return "haha";
	var x = $(id);
	var y = "";
	for (i=0; i<x.length; i++){	
		y += x.options[i].text;
		y += "\n";
	}
	return y;
}
