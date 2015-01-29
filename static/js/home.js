$(document).ready(function(){
	var igualop = '';
	var iguali = 0;
	var igualops = ['=op', '<strong>=op</strong>', '<ins>=op</ins>', '<small>=op</small>', '<i>=op</i>', '<del>=op</del>']

	igualf = function() {
		var i = iguali % igualops.length;
		igualop += igualops[i] + ' ';
		iguali++;
		$('#igualop').html(igualop);
	};

	setInterval(igualf, 50);
});
