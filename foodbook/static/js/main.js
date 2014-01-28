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
  var dimOverlay = document.getElementById('dim-overlay');
  var triangleImg = document.getElementById('triangle');
  var open = 'navbar-open';
  var close = 'navbar-closed';
	toggleClass(navbar, open);
	toggleClass(navbarButton, open);
  toggleClass(dimOverlay, open);
  toggleClass(triangle, open);
	if (hasClass(navbar, open)) {
		removeClass(navbar, close);
		removeClass(navbarButton, close);
    removeClass(dimOverlay, close);
    removeClass(triangle, close);
	} else {
		addClass(navbar, close);
		addClass(navbarButton, close);
    addClass(dimOverlay, close);
    addClass(triangle, close);
	}
}

$(document).ready(function(){
	var image = document.getElementById('login-pic');
	resizeImage(50, image);
	searchResult();
	handleSearch();
});


var handleSearch = function() {
	$("#global-search").keyup(function(event){
	    if(event.keyCode == 13){
	    	var username = document.getElementById('global-search').value;
	    	window.location = '/user/' + username;
	    }
	});
}

/**
 * Resizes the image based on the threshold
 */
var resizeImage = function(threshold, image) {
	var height = image.naturalHeight;
	var width = image.naturalWidth;
	if (height > threshold && width > threshold) {
		if (height > width) {
			image.style.width = threshold + 'px';
			image.style.top = -(height * threshold/width) / 2 + 'px';
		} else {
			image.style.height = threshold + 'px'
			image.style.left = -(width * threshold/height - threshold) / 2 + 'px';
		}
	}
	else if(height > threshold){
		image.style.left = -(width * threshold/height - threshold) / 2 + 'px';
		image.style.top = -(height * threshold/width) / 2 + 'px';
	}
	else if(width > threshold){
		image.style.left = -(width * threshold/height - threshold) / 2 + 'px';
		image.style.top = -(height * threshold/width) / 2 + 'px';
	}
	else{
		image.style.top = -(height * threshold/width) / 2 + 'px';
		image.style.left = -(width * threshold/height - threshold) / 2 + 'px';
	}
}

// Global functions
// Handlers for responsive fields

$('#global-search').focus(function(){
	$('#global-search').css('background-color', '#FFFFFF');
	$('#header-search').css('background-color', '#FFFFFF');
});

$('#global-search').focusout(function(){
	$('#global-search').css('background-color', '#F1F1F1');
	$('#header-search').css('background-color', '#F1F1F1');
});

$('#header-search').hover(function(){
	$('#global-search').css('background-color', '#FFFFFF');
	$('#header-search').css('background-color', '#FFFFFF');
}, function(){
	if(!$('#global-search').is(':focus')){
		$('#global-search').css('background-color', '#F1F1F1');
		$('#header-search').css('background-color', '#F1F1F1');
}});

var save_diet = function(){
	var description = $('#diet-description').val()
	var calories = $('#diet-calories').val()
	var fat = $('#diet-fat').val()
	var sugar = $('#diet-sugar').val()
	var protein = $('#diet-protein').val()
	Dajaxice.diet.update(confirm_save, {'restrictions': description, 'calories': calories, 'fat': fat, 'sugar': sugar, 'protein': protein});
}

function confirm_save(data){
	if(data.success){
		$('#recipe-id-unique').val(data.rid);
		alert("Save successful.");
	}
	else{
		alert("Save failed.");
	}
}

var redirect = function(){
	window.location.replace('/recipe/add');
}

var removeBox = function(div) {
	$(div).parent().parent().hide();
}


var searchResult = function() {
    $("#global-search").autocomplete({
	  source: '/search.json',
      focus: function( event, ui ) {
        $( "#global-search" ).val( ui.item.label );
        return false;
      },
	}).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
      return $("<li>" )
        .append("<a href = '/user/" + item.label + "'>" + item.label + "</a>")
        .appendTo( ul );
 	};
 	$("#global-search").data( "ui-autocomplete")._resizeMenu = function() {
  		this.menu.element.outerWidth( 550 );
	};
 	$("#global-search").data( "ui-autocomplete")._renderMenu = function(ul, items) {
	  var that = this;
	  $.each( items, function( index, item ) {
	    that._renderItemData( ul, item );
	  });
	  $(ul).css("border-radius", "0px");
	  $(ul).find("a").css("border-radius", "0px");
	  var find = $(ul).find("a");
	  find.hover(function(){
	  });
	};
}
