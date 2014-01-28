var retrieve_posts = function(num){
	Dajaxice.comment.user_get(confirm_resize, {'username': $('#username').val(), 'num': num});
	return false;
}

var confirm_resize = function(data){
	Dajax.process(data);
	resizeImages();
}

var resizeImages = function(){
	var elements = document.getElementsByClassName('poster-img');
	for(var i = 0; i < elements.length; i++){
		elements[i].onload = function(){
			resizeImage(26, this);
		};
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
	retrieve_posts(5);
	document.getElementById('profile-image-img').onload = function(){
		resizeImage(150, this);
	};
	resizeImage(150, document.getElementById('profile-image-img'));
	load_recipes('name', 0);
}

var comments = function() {
	addClass(document.getElementById('profile-content-container'), 'selected');
	removeClass(document.getElementById('profile-recipe-container'), 'selected');
}

var recipes = function() {
	removeClass(document.getElementById('profile-content-container'), 'selected');
	addClass(document.getElementById('profile-recipe-container'), 'selected');
}

var load_recipes = function(param, num){
	Dajaxice.recipe.list_all(Dajax.process, {'param': param, 'page': num, 'username': $('#username').val()});
	return false;
}