var toggleCheckbox = function() {
	var dietCB = document.getElementById('diet-checkmark');
	toggleClass(dietCB, 'enabled');
}

var viewAll = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'vr-mine') {
		removeClass(selectedDiv, 'selected');
		addClass(document.getElementById('vr-all'), 'selected');
	}
}

var viewMine = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'vr-all') {
		removeClass(selectedDiv, 'selected');
		addClass(document.getElementById('vr-mine'), 'selected');
	}
}