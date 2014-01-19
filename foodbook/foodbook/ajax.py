from dajax.core import Dajax
import json
from foodbook.models import Ingredient
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