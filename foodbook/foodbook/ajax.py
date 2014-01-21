from dajax.core import Dajax
import json
from foodbook.models import Ingredient, ServingSize, Recipe
from dajaxice.decorators import dajaxice_register

@dajaxice_register(method='GET', name='ingredient.update')
def update_search(request, div_id, search, search_type="All"):
	dajax = Dajax()
	if search_type != "All":
		ingredients = Ingredient.objects.filter(name__istartswith=search, ingredient_type__name__iexact=search_type)
	else:
		ingredients = Ingredient.objects.filter(name__istartswith=search)
	out = []
	for ingredient in ingredients:
		next = "<a href='/ingredients/%s' id='ingredient_num_%s'>%s " % (ingredient.name, ingredient.id, ingredient.name)
		if ingredient.modifier:
			next += "(%s)" % ingredient.modifier
		next += "</a><br/>"
		out.append(next)

	dajax.assign('#' + div_id, 'innerHTML', "".join(out))
	return dajax.json()

@dajaxice_register(method='GET', name='ingredient.update_url')
def update_recipe_ingredient_search(request, div_id, search, search_type="All"):
	dajax = Dajax()
	if search_type != "All":
		ingredients = Ingredient.objects.filter(name__istartswith=search, ingredient_type__name__iexact=search_type)
	else:
		ingredients = Ingredient.objects.filter(name__istartswith=search)
	out = []
	for ingredient in ingredients:
		next = "<a href='#' id='ingredient_num_%s' onclick='add_ingredient(%s)'>%s " % (ingredient.name, ingredient.id , ingredient.name)
		if ingredient.modifier:
			next += "(%s)" % ingredient.modifier
		next += "</a><br/>"
		out.append(next)

	dajax.assign('#' + div_id, 'innerHTML', "".join(out))
	return dajax.json()

@dajaxice_register(method='GET', name='recipe.add_ingredient')
def add_ingredient(request, iid):
	dajax = Dajax()
	ingredient = Ingredient.objects.get(id__exact=iid)
	serving_sizes = ingredient.servingsize_set.all()
	out = []
	out.append("%s <input type='number' id='ingredient_line_%s_number'/> <select id='ingredient_line_%s_select'>" % (ingredient.name, ingredient.id, ingredient.id))
	for ss in serving_sizes:
		next = "<option value='%s'>%s </option>" % (ss.name, ss.name)
		out.append(next)
	out.append("</select>")

	return json.dumps({'html': "".join(out), 'id': ingredient.id})

@dajaxice_register(method='POST', name='recipe.save')
def save_recipe(request, rid, ingredients):
	if(request.user.is_authenticated):
		if rid:
			recipe = Recipe.objects.get(id=rid, user_id=request.user)
			if recipe:
				recipe.ingredients = json.dumps(ingredients)
				recipe.save()
			else:
				return json.dumps({'success': False})
		else:
			recipe = Recipe(name="Untitled Recipe", ingredients=json.dumps(ingredients), upvotes=0)
			recipe.save()
			recipe.user_id.add(request.user)
	return json.dumps({'success': True})