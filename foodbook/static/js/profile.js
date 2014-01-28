var post_number = 5;

var retrieve_posts = function(){
	Dajaxice.comment.user_get(Dajax.process, {'username': $('#username').val()});
	return false;
}

var resizeImages = function(){
	var elements = document.getElementsByClassName('poster-img');
	for(var i = 0; i < elements.length; i++){
	resizeImage(26, elements[i]);
	}
}

var add_comment = function(){
	Dajaxice.comment.user_add(Dajax.process, {'username': $('#username').val(), 'comment': $('#comment-box').val()});
	return false;
}

window.onload = function(event) {
	$('#profile-image-edit').click(function(){
		$('#id_image').click();
	});
	$('#id_image').change(function(){
		document.getElementById('profile-pic-form').submit();
	})
	retrieve_posts();
	resizeImage(150, document.getElementById('profile-image-img'));
}

var comments = function() {
	addClass(document.getElementById('profile-content-container'), 'selected');
	removeClass(document.getElementById('profile-recipe-container'), 'selected');
}

var recipes = function() {
	removeClass(document.getElementById('profile-content-container'), 'selected');
	addClass(document.getElementById('profile-recipe-container'), 'selected');
}