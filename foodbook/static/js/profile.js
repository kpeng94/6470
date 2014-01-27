var post_number = 5;

var retrieve_posts = function(){
	Dajaxice.comment.user_get(Dajax.process, {'username': $('#username').val()});
	return false;
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