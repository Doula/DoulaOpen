var Application = {

    init: function() {
    	this.bindDataActions();
    	this.bindUIActions();
    },

    bindUIActions: function() {
    	$('.sm-side-tab').sideTab();

    	$('#add-note-link').on('click', function() {
    		$('#add-note-div').toggleClass('hide');
    		return false;
    	});
    },

    bindDataActions: function() {

    }
};

$(document).ready(function() {
  Application.init();
});