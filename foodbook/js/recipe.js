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

function show_ingredient(data){
	var div_elem = document.createElement("div");
	div_elem.class = 'ingredient-line';
	div_elem.id = 'ingredient_line_' + data.id;
	div_elem.innerHTML = data.html;
	$('#recipe-list').append(div_elem);
}

function check_ingredient(){
	chosen_ingredients = $('#recipe-list').children();
	for(var i=0; i < chosen_ingredients.length; i++) {
		var id = Number(chosen_ingredients[i].getAttribute('id').match('[0-9]+')[0]);
		if(iid_l.indexOf(id) == -1)
			iid_l.push(id);
	}
}

function add_ingredient(iid){
	check_ingredient();
	if(iid_l.indexOf(iid) != -1)
		return false;
	Dajaxice.recipe.add_ingredient(show_ingredient, {'iid': iid.toString()});
	iid_l.push(iid);
	return true;
}

function clear_cache(){
	cache_list.id = [];
	cache_list.qty = [];
	cache_list.unit = [];
}

function summary_ingredients(){
	clear_cache();
	chosen_ingredients = $('#recipe-list').children();
	for(var i=0; i < chosen_ingredients.length; i++) {
		var id = chosen_ingredients[i].getAttribute('id').match('[0-9]+')[0];
		var line = "#ingredient_line_" + id;
		cache_list.id.push(id);
		cache_list.qty.push($(line + "_number").val());
		cache_list.unit.push($(line + "_select").val());
	}
}

function confirm_save(data){
	if(data.success){
		alert("Save successful.");
	}
	else{
		alert("Save failed.");
	}
}

function save_recipe(){
	var id = $('#recipe-id-unique').val();
	summary_ingredients();
	Dajaxice.recipe.save(confirm_save, {'rid': id, 'ingredients': cache_list});
	return false;
}

function check_nutrients(){
	summary_ingredients();
	Dajaxice.recipe.check(test, {'ingredients': cache_list});
	return false;
}

function test(data){
	alert(data);
}

window.onload = function(e){
	perform_search();	
}