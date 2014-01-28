var selected_type = "All";
var iid_l = new Array();
var cache_list = {
	id: [],
	qty: [],
	unit: []
};

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

function check_ingredient(){
	chosen_ingredients = $('#recipe-list').children();
	for(var i=0; i < chosen_ingredients.length; i++) {
		var matchElement = chosen_ingredients[i].getAttribute('id');
		if (matchElement != null) {
			var id = Number(matchElement.match('[0-9]+')[0]);
			if(iid_l.indexOf(id) == -1)
				iid_l.push(id);
		}
	}
}

function clear_cache(){
	cache_list.id = [];
	cache_list.qty = [];
	cache_list.unit = [];
}

function summary_ingredients(){
	clear_cache();
	chosen_ingredients = $('#nr-ingredients-content').children();
	for(var i=0; i < chosen_ingredients.length; i++) {
		var id = chosen_ingredients[i].getAttribute('id').match('[0-9]+')[0];
		var line = "#ingredient_line_" + id;
		cache_list.id.push(id);
		cache_list.qty.push(Number($(line + "_number").html()));
		cache_list.unit.push($(line + "_select").html().trim());
	}
}

function check_nutrients(){
	summary_ingredients();
	Dajaxice.recipe.check(modify_nutrients, {'ingredients': cache_list, 'ss': $('#nrecipe-serving-size').html()});
	return false;
}

function modify_nutrients(data){
	for(key in data){
		$('#' + key + '-num').html(Number(data[key][0]).toFixed(1));
		var percentage = Number(data[key][1]);
		if(percentage > 100)
			percentage = 100;
		$('#' + key + ' div span').width(percentage + '%');
	}
}

var update_nutrients = function(){
	if($(this).val() == "" || isNaN($(this).val())){
		$(this).val('1');
	}
	check_nutrients();
}

window.onload = function(e){
	check_nutrients();
	retrieve_posts(5);
}

var getTextWidth = function(div) {
	var width = (div.clientWidth + 1);
	return width;
};

var centerText = function(div, outerDiv) {
	var outerWidth = outerDiv.offsetWidth;
	var width = getTextWidth(div);
	var margin = (outerWidth - width) / 2;
	div.style.marginLeft = margin + 'px';
	div.style.marginRight = margin + 'px';
};

var add_comment = function(){
	Dajaxice.comment.recipe_add(Dajax.process, {'rid': $('#rid').val(), 'comment': $('#comment-box').val()});
	return false;
}

var retrieve_posts = function(num){
	Dajaxice.comment.recipe_get(confirm_resize, {'rid': $('#rid').val(), 'num': num});
	return false;
}

var upvote = function(){
	Dajaxice.recipe.upvote(Dajax.process, {'rid': $('#rid').val()});
	return false;
}

var downvote = function(){
	Dajaxice.recipe.downvote(Dajax.process, {'rid': $('#rid').val()});
	return false;
}