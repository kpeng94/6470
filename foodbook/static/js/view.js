var toggleCheckbox = function() {
	var dietCB = document.getElementById('diet-checkmark');
	toggleClass(dietCB, 'enabled');
}

var viewAll = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'vr-mine') {
		removeClass(selectedDiv, 'selected');
		removeClass(document.getElementById('vr-view-mine'), 'clicked');
		addClass(document.getElementById('vr-all'), 'selected');
		addClass(document.getElementById('vr-view-all'), 'clicked');
	}
}

var viewMine = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'vr-all') {
		removeClass(selectedDiv, 'selected');
		removeClass(document.getElementById('vr-view-all'), 'clicked');
		addClass(document.getElementById('vr-mine'), 'selected');
		addClass(document.getElementById('vr-view-mine'), 'clicked');
	}
}

var load_my_recipes = function(param){
	Dajaxice.recipe.list_mine(Dajax.process, {'param': param});
	return false;
}

window.onload = function(event) {
	load_my_recipes('name');
}