

window.onload = function(event) {
	$('#profile-image-edit').click(function(){
		$('#id_image').click();
	});
	$('#id_image').change(function(){
		document.getElementById('profile-pic-form').submit();
	})
	resizeImage(150, document.getElementById('profile-image-img'));
}