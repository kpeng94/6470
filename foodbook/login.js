// Login fields

$('#id_username').focus(function(){
	$('#id_username').css('background-color', '#FFFFFF');
});

$('#id_username').focusout(function(){
	$('#id_username').css('background-color', '#F1F1F1');
});

$('.login-username').hover(function(){
	$('#id_username').css('background-color', '#FFFFFF');
}, function(){
	if(!$('#id_username').is(':focus')){
		$('#id_username').css('background-color', '#F1F1F1');
}}); 

$('#id_password').focus(function(){
	$('#id_password').css('background-color', '#FFFFFF');
});

$('#id_password').focusout(function(){
	$('#id_password').css('background-color', '#F1F1F1');
});

$('.login-password').hover(function(){
	$('#id_password').css('background-color', '#FFFFFF');
}, function(){
	if(!$('#id_password').is(':focus')){
		$('#id_password').css('background-color', '#F1F1F1');
}});