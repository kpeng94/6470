var selected_type = "All";
var iid_l = new Array();
var cache_list = {
	id: [],
	qty: [],
	unit: []
};

function change_search(ingredient_type){
	selected_type = ingredient_type;
	perform_search()
	return false;
}

function perform_search(){
	Dajaxice.ingredient.update_url(Dajax.process, {'search':$('#ingredient-search').val(), 'div_id': 'ingredient-list', 'search_type': selected_type});
	return false;
}

function update_page(num){
	Dajaxice.ingredient.update_url(Dajax.process, {'search': $('#ingredient-search').val(), 'div_id': 'ingredient-list', 'search_type': selected_type, 'page': num});
	return false;
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
	chosen_ingredients = $('#recipe-list').children();
	for(var i=1; i < chosen_ingredients.length; i++) {
		var id = chosen_ingredients[i].getAttribute('id').match('[0-9]+')[0];
		var line = "#ingredient_line_" + id;
		cache_list.id.push(id);
		cache_list.qty.push($(line + "_number").val());
		cache_list.unit.push($(line + "_select").val());
	}
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

function save_recipe(){
	var id = $('#recipe-id-unique').val();
	var description = $('#recipe-description').val();
	var instructions = $('#recipe-instructions').val();
	var name = $('#recipe-name-i').val();
	var ss = $('#recipe-serving-size').val();
	var makepublic = document.getElementById('recipe-public').checked
	var suggestions = $('#recipe-suggestions').val()
	summary_ingredients();
	Dajaxice.recipe.save(confirm_save, {'rid': id, 'ss': ss, 'public': makepublic, 'ingredients': cache_list, 'name': name, 'description': description, 'instructions': instructions, 'suggestions': suggestions});
	return false;
}

function check_nutrients(){
	summary_ingredients();
	Dajaxice.recipe.check(modify_nutrients, {'ingredients': cache_list, 'ss': $('#recipe-serving-size').val()});
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

var check_input = function(){
	if($(this).val() == "" || isNaN($(this).val())){
		$(this).val('1');
	}
}

var update_nutrients = function(){
	if($(this).val() == "" || isNaN($(this).val())){
		$(this).val('1');
	}
	check_nutrients();
}

window.onload = function(e){
	perform_search();
	$('#recipe-serving-size').blur(update_nutrients);
	check_nutrients();
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

var nextContent = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'recipe-info') {
		removeClass(selectedDiv, 'selected');
		addClass(document.getElementById('recipe-instructions-and-descriptions'), 'selected');
		addClass(document.getElementById('recipe-prev'),'clickable');
		removeClass(document.getElementById('recipe-next'), 'clickable');
	}
};

var previousContent = function() {
	var selectedDiv = document.getElementsByClassName('selected')[0];
	if (selectedDiv.id == 'recipe-instructions-and-descriptions') {
		removeClass(selectedDiv, 'selected');
		addClass(document.getElementById('recipe-info'),
										 'selected');
		removeClass(document.getElementById('recipe-prev'),'clickable');
		addClass(document.getElementById('recipe-next'),'clickable');
	}
};

function show_ingredient(data){
	var div_elem = document.createElement("div");
	div_elem.className = 'ingredient-line';
	div_elem.id = 'ingredient_line_' + data.id;
	div_elem.innerHTML = data.html;
	$('#recipe-list').append(div_elem);
	$('#ingredient_line_' + data.id + '_number').blur(update_nutrients);
	$('#ingredient_line_' + data.id + '_select').change(check_nutrients);
	check_nutrients();
}

function add_ingredient(iid){
	check_ingredient();
	if(iid_l.indexOf(iid) != -1)
		return false;
	Dajaxice.recipe.add_ingredient(show_ingredient, {'iid': iid.toString()});
	iid_l.push(iid);
	return true;
}

var jimmyWu = function(element) {
	var div = element.parentNode;
	div.parentNode.removeChild(div);
}