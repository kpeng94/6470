from dajax.core import Dajax
import json
from foodbook.models import Ingredient
from dajaxice.decorators import dajaxice_register

@dajaxice_register(method='GET', name='ingredient.update')
def update_search(request, search):
	dajax = Dajax()
	ingredients = Ingredient.objects.filter(name__istartswith=search)
	out = []
	for ingredient in ingredients:
		out.append("<a href='/ingredients/%s'>%s</a><br/>" % (ingredient.name, ingredient.name))

	dajax.assign('#ingredient-list', 'innerHTML', "".join(out))
	return dajax.json()