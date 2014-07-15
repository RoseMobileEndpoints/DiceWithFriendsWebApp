/* Namespace */
var rh = rh || {};
rh.dwf = rh.dwf || {};
rh.dwf.home = rh.dwf.home || {};

rh.dwf.home.enableButtons = function() {
	$("#new-game-btn").click(function() {
		$('input[name=player2_email]').val("");
	    $('#new-game-modal').modal('show');
	});
};

/* main */
$(document).ready( function() {
	rh.dwf.home.enableButtons();
});