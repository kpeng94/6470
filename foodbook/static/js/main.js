/**
 * Adds a class to a div element.
 * @param div Div element to add the class to
 * @param name Class name to add
 */
var addClass = function(div, name) {
	div.classList.add(name);
}

/**
 * Removes a class from a div element.
 * @param div Div element to remove the class from
 * @param name Class name to remove
 */
var removeClass = function(div, name) {
	div.classList.remove(name);
}

/**
 * Checks whether the div has a class.
 * @param div Div element to check
 * @param name Class name to check
 * @return True if the div has the class, false otherwise.
 */
var hasClass = function(div, name) {
	if(div.classList.contains(name)) {
		return true;
	} else {
		return false;
	}
}

var toggleClass = function(div, name) {
	if (hasClass(div, name)) {
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

var showToolbar = function() {
	addClass(document.getElementById('main-navbar'), 'navbar-open');
	addClass(document.getElementById('nav-button'), 'navbar-open');
}

var hideToolbar = function() {
	removeClass(document.getElementById('main-navbar'), 'navbar-open');
	removeClass(document.getElementById('nav-button'), 'navbar-open');
}

/**
 *
 */
var toggleToolbar = function() {
	var navbar = document.getElementById('main-navbar');
	var navbarButton = document.getElementById('nav-button');
	toggleClass(navbar, 'navbar-open');
	toggleClass(navbarButton, 'navbar-open');
	if (hasClass(navbar, 'navbar-open')) {
		removeClass(navbar, 'navbar-closed');
		removeClass(navbarButton, 'navbar-closed');
	} else {
		addClass(navbar, 'navbar-closed');
		addClass(navbarButton, 'navbar-closed');
	}
}

// Global functions

// document.getElementsByClassName('login-icon')[0].addEventListener('click', toggleLoginVisibility, false);

