/**
 * @param div Div element to add the class to
 * @param div Name class name to add
 */
var addClass = function(div, name) {
	div.classList.add(name);
}

/**
 * @param div Div element to remove the class from
 * @param
 */
var removeClass = function(div, name) {
	div.classList.remove(name);
}

var toggleClass = function(div, name) {
	if (div.classList.contains(name)) {
		removeClass(div, name);
	} else {
		addClass(div, name);
	}
}

var showLogin = function() {
	addClass(document.getElementsByClassName('login')[0]('login'), 'visible');
}

var hideLogin = function() {
	removeClass(document.getElementsByClassName('login')[0]('login'), 'visible');
}

var toggleLoginVisibility = function() {
	toggleClass(document.getElementsByClassName('login')[0], 'visible');
}

// Global functions

// document.getElementsByClassName('login-icon')[0].addEventListener('click', toggleLoginVisibility, false);

