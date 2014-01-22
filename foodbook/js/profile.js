var resizeProfileContent = function() {
	// Resize half circle
	var profileContentBackground = document.getElementById('profile-content-background');
	var profileContent = document.getElementById('profile-half-circle');
	var width = profileContentBackground.offsetWidth;
	var margin = (width - 100) / 2;
	profileContent.style.marginLeft = margin;
	profileContent.style.marginRight = margin;
	profileContent.style.display = 'block';
}

window.onload = function(event) {
	resizeProfileContent();
}