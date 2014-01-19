var selected_type = "All"

function change_search(ingredient_type){
	selected_type = ingredient_type;
	perform_search()
	return false;
}

function perform_search(){
	Dajaxice.ingredient.update(Dajax.process, {'search':document.getElementById('ingredient-search').value, 'div_id': 'ingredient-list', 'search_type': selected_type});
	return false;
}

window.onload = function(e){
	perform_search();
}