from dajax.core import Dajax
import json, decimal
from foodbook.models import Ingredient, ServingSize, Recipe, UserDiet, Comment, UserPicture, IngredientWrapper
from dajaxice.decorators import dajaxice_register
from recipe_utils import calculate_nutritional_value, decimal_json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.db.models import Q
from django.template.defaultfilters import timesince

@dajaxice_register(method='GET', name='ingredient.update')
def update_search(request, div_id, search, search_type="All"):
	dajax = Dajax()
	if search_type == "All":
		ingredients = Ingredient.objects.filter(name__icontains=search)
	elif search_type == "Meat":
		ingredients = Ingredient.objects.filter(Q(ingredient_type__name__iexact='Pork') | Q(ingredient_type__name__iexact='Beef') | Q(ingredient_type__name__iexact='Lamb') | Q(ingredient_type__name__iexact='Chicken'), name__icontains=search).order_by(name)
	else:
		ingredients = Ingredient.objects.filter(name__icontains=search)
	out = []
	for ingredient in ingredients:
		next = "<div class='ingredient'><a href='/ingredients/%s' class='ingredient-link' id='ingredient_num_%s'>%s " % (ingredient.id, ingredient.id, ingredient.name)
		if ingredient.modifier:
			next += "(%s)" % ingredient.modifier
		next += "</a></div>"
		out.append(next)

	dajax.assign('#' + div_id, 'innerHTML', "".join(out))
	return dajax.json()

@dajaxice_register(method='GET', name='ingredient.update_url')
def update_recipe_ingredient_search(request, div_id, search, page='0', num_per_page=15, search_type="All"):
	dajax = Dajax()
	page = int(page)
	if search_type == "All":
		ingredients = Ingredient.objects.filter(name__icontains=search)
	elif search_type == "meat":
		ingredients = Ingredient.objects.filter(Q(ingredient_type__name__iexact='Pork') | Q(ingredient_type__name__iexact='Beef') | Q(ingredient_type__name__iexact='Lamb') | Q(ingredient_type__name__iexact='Chicken'), name__icontains=search).order_by('name')
	elif search_type == 'seafood':
		ingredients = Ingredient.objects.filter(Q(ingredient_type__name__iexact='Fish') | Q(ingredient_type__name__iexact='Shellfish'), name__icontains=search).order_by('name')	
	elif search_type == 'nuts-and-legumes':
		ingredients = Ingredient.objects.filter(Q(ingredient_type__name__iexact='Nuts') | Q(ingredient_type__name__iexact='Legumes') | Q(ingredient_type__name__iexact='Seeds') | Q(ingredient_type__name__iexact='Soy'), name__icontains=search).order_by('name')	
	elif search_type == 'dairy-and-eggs':
		ingredients = Ingredient.objects.filter(Q(ingredient_type__name__iexact='Dairy') | Q(ingredient_type__name__iexact='Eggs'), name__icontains=search).order_by('name')	
	elif search_type == 'soups-and-sauces':
		ingredients = Ingredient.objects.filter(ingredient_type__name__iexact='Soups and Sauces', name__icontains=search).order_by('name')
	elif search_type == 'spices-and-herbs':
		ingredients = Ingredient.objects.filter(ingredient_type__name__iexact='Spices and Herbs', name__icontains=search).order_by('name')
	elif search_type == 'fats-and-oils':
		ingredients = Ingredient.objects.filter(ingredient_type__name__iexact='Fats and Oils', name__icontains=search).order_by('name')	
	else:
		ingredients = Ingredient.objects.filter(name__icontains=search, ingredient_type__name__iexact=search_type)
	count = ingredients.count()
	ingredients = ingredients.order_by('name')[page*num_per_page:(page+1)*num_per_page]
	out = []
	for ingredient in ingredients:
		next = "<div class='ingredient-%s'><div class = 'ingredient-expanded-name'>%s " % (ingredient.ingredient_type.name.encode('ascii', 'ignore').lower().split('/')[0], ingredient.name)
		if ingredient.modifier:
			next += "(%s)" % ingredient.modifier
		next += "</div><a href='javascript:void(0);' class='ingredient-link' id='ingredient_num_%s' onclick='add_ingredient(%s)'>%s " % (ingredient.id, ingredient.id , ingredient.name)
		if ingredient.modifier:
			next += "(%s)" % ingredient.modifier
		next += "</a></div>"
		out.append(next)

	out.append('<div id = "il-previous-next">');
	if page != 0:
		out.append('<div id = "il-previous" class = "prev clickable" onclick="update_page(%d)"><i class = "fa fa-chevron-left"></i></div>' % (page-1))
	else:
		out.append('<div id = "il-previous" class = "prev"><i class = "fa fa-chevron-left"></i></div>')
	if page != count/num_per_page:
		out.append('<div id = "il-next" class = "next clickable" onclick="update_page(%d)"><i class = "fa fa-chevron-right"></i></div>' % (page+1))
	else:
		out.append('<div id = "il-next" class = "next"><i class = "fa fa-chevron-right"></i></div>')

	out.append('</div>')

	dajax.assign('#' + div_id, 'innerHTML', "".join(out))
	return dajax.json()

@login_required
@dajaxice_register(method='GET', name='recipe.add_ingredient')
def add_ingredient(request, iid):
	dajax = Dajax()
	ingredient = Ingredient.objects.get(id__exact=iid)
	serving_sizes = ingredient.servingsize_set.all()
	out = []
	out.append("<div class='ingredient-name'>%s (%s)</div><div class='ingredient-input-div'><input type='number' value=1 id='ingredient_line_%s_number'/> </div><div class='ingredient-select-div'><select class='ingredient-select' id='ingredient_line_%s_select'>" % (ingredient.name, ingredient.modifier, ingredient.id, ingredient.id))
	for ss in serving_sizes:
		next = "<option value='%s'>%s </option>" % (ss.name, ss.name)
		out.append(next)
	out.append("</select>")
	out.append("</div>")

	return json.dumps({'html': "".join(out), 'id': ingredient.id})

@dajaxice_register(method='POST', name='recipe.save')
def save_recipe(request, rid, ingredients, name, description, suggestions, instructions, ss, public):
	if request.user.is_authenticated():
		nutrients = calculate_nutritional_value(ingredients, request.user, ss)
		halal = False
		lacto = False
		lactoovo = False
		vegan = False
		diabetes = False
		hypertension = False
		nuts = False
		lactose = False
		eggs = False
		soy = False
		shellfish = False
		fish = False
		ingredient_list = []
		for i in xrange(len(ingredients['id'])):
			ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
		for ingredient in ingredient_list:
			if ingredient.type == 'Pork' or 'pork' in ingredient.restrictions:
				halal = True
				vegan = True
				lactoovo = True
				lacto = True
			elif ingredient.type == 'Dairy' or 'dairy' in ingredient.restrictions:
				lactose = True
				vegan = True
			elif ingredient.type == 'Eggs' or 'eggs' in ingredient.restrictions:
				vegan = True
				lacto = True
				eggs = True
			elif ingredient.type == 'Fish' or 'fish' in ingredient.restrictions:
				vegan = True
				lacto = True
				lactoovo = True
				fish = True
			elif ingredient.type == 'Beef' or ingredient.type=='Chicken' or ingredient.type == 'Lamb':
				vegan = True
				lacto = True
				lactoovo = True
			elif ingredient.type == 'Soy' or 'soy' in ingredient.restrictions:
				soy = True
			elif ingredient.type == 'Nuts' or 'nuts' in ingredient.restrictions:
				nuts = True
			elif ingredient.type == 'Shellfish' or 'shellfish' in ingredient.restrictions:
				shellfish = True
		if nutrients['carbohydrates'][1] > decimal.Decimal(66):
			diabetes = True
		if nutrients['total-fat'][1] > decimal.Decimal(66) or nutrients['sodium'][1] > decimal.Decimal(80):
			hypertension = True
		if rid:
			try:
				recipe = Recipe.objects.get(id=rid, user_id=request.user)
			except:
				return json.dumps({'success': False})
		# IF RECIPE EXISTS
			recipe.name = name
			recipe.description = description
			recipe.servings = ss
			recipe.instructions = instructions
			recipe.ingredients_text = json.dumps(ingredients)
			recipe.calories = nutrients['calories'][0]
			recipe.total_fat = nutrients['total-fat'][0]
			recipe.saturated_fat = nutrients['saturated'][0]
			recipe.polyunsaturated_fat = nutrients['polyunsaturated'][0]
			recipe.monounsaturated_fat = nutrients['monounsaturated'][0]
			recipe.trans_fat = nutrients['trans'][0]
			recipe.cholesterol = nutrients['cholesterol'][0]
			recipe.sodium = nutrients['sodium'][0]
			recipe.potassium = nutrients['potassium'][0]
			recipe.total_carbohydrates = nutrients['carbohydrates'][0]
			recipe.dietary_fiber = nutrients['fiber'][0]
			recipe.sugar = 0
			recipe.protein = nutrients['protein'][0]
			recipe.vitamin_a = nutrients['vita'][0]
			recipe.vitamin_b_6 = nutrients['vitb6'][0]
			recipe.vitamin_b_12 = nutrients['vitb12'][0]
			recipe.calcium = nutrients['calcium'][0]
			recipe.iron = nutrients['iron'][0]
			recipe.vitamin_d = nutrients['vitd'][0]
			recipe.magnesium = nutrients['magnesium'][0]
			recipe.public = public
			recipe.suggested = suggestions
			recipe.halal = halal
			recipe.lacto = lacto
			recipe.lactoovo = lactoovo
			recipe.vegan = vegan
			recipe.diabetes = diabetes
			recipe.hypertension = hypertension
			recipe.nuts = nuts
			recipe.lactose = lactose
			recipe.eggs = eggs
			recipe.soy = soy
			recipe.shellfish = shellfish
			recipe.fish = fish
			recipe.save()
		# NO RID
		else:
			recipe = Recipe(name=name, user_id = request.user, servings = ss, description=description, instructions=instructions, ingredients_text=json.dumps(ingredients), upvotes=0,
				calories = nutrients['calories'][0], total_fat = nutrients['total-fat'][0], saturated_fat = nutrients['saturated'][0], polyunsaturated_fat = nutrients['polyunsaturated'][0],
				monounsaturated_fat = nutrients['monounsaturated'][0], trans_fat = nutrients['trans'][0], cholesterol = nutrients['cholesterol'][0], sodium = nutrients['sodium'][0], 
				potassium = nutrients['potassium'][0], total_carbohydrates = nutrients['carbohydrates'][0], dietary_fiber = nutrients['fiber'][0], 
				sugar=0, protein = nutrients['protein'][0], vitamin_a = nutrients['vita'][0], vitamin_b_6 = nutrients['vitb6'][0], vitamin_b_12 = nutrients['vitb12'][0],
				vitamin_c=nutrients['vitc'][0], calcium = nutrients['calcium'][0], iron=nutrients['iron'][0], vitamin_d = nutrients['vitd'][0], magnesium = nutrients['magnesium'][0], public=public, suggested=suggestions,
				halal=halal, lacto=lacto, lactoovo=lactoovo, diabetes=diabetes, vegan=vegan, hypertension=hypertension, nuts=nuts, lactose=lactose, eggs=eggs, soy=soy, shellfish=shellfish,
				fish=fish)
			recipe.save()
			rid = recipe.id
	return json.dumps({'success': True, 'rid': rid})

@dajaxice_register(method='GET', name='recipe.check')
def check_nutrients(request, ingredients, ss):
	try:
		ss = decimal.Decimal(ss)
	except:
		ss = decimal.Decimal(1)
	if request.user.is_authenticated():
		return json.dumps(calculate_nutritional_value(ingredients, request.user, ss), default=decimal_json)

@dajaxice_register(method='POST', name='diet.update')
def update_diet(request, restrictions, calories, fat, sugar, protein):
	if request.user.is_authenticated():
		try:
			diet = UserDiet.objects.get(user=request.user)
			diet.diet_description = restrictions
			diet.calories = calories
			diet.fat = fat
			diet.sugar = sugar
			diet.protein = protein
			diet.save()
			return json.dumps({'success': True})
		except:
			diet = UserDiet(user=request.user, diet_description=restrictions, calories=calories, fat=fat, sugar=sugar, protein=protein)
			diet.save()
			return json.dumps({'success': True})
		return json.dumps({'success': False})

@login_required
@dajaxice_register(method='POST', name='comment.user_add')
def add_comment(request, username='', comment=''):
	dajax = Dajax()
	if username == '' or username == request.user.username:
		messages.error(request, "Sadly, you can't add comments to your own profile.")
		dajax.redirect('/user')
		return dajax.json()
	else:
		try:
			user = User.objects.get(username=username)
		except:
			messages.error(request, "That user doesn't exist.")
			dajax.redirect(request.META['HTTP_REFERER'])
			return dajax.json()
	if comment == '':
		messages.error(request, "Your comments have to actually say something.")
		dajax.redirect(request.META['HTTP_REFERER'])
		return dajax.json()
	comment = Comment(original_poster=request.user, receiving_user=user, comment=comment)
	comment.save()
	messages.success(request, "Comment posted successfully!")
	dajax.redirect(request.META['HTTP_REFERER'])
	return dajax.json()

@dajaxice_register(method='POST', name='comment.user_get')
def get_comments(request, username='', num=5):
	dajax = Dajax()
	try:
		num = int(num)
	except:
		messages.error(request, "Stop playing around with the Javascript!")
		dajax.redirect(request.META['HTTP_REFERER'])
		return dajax.json()
	if num < 0:
		num = 5
	if username == '':
		username = request.user.username
	try:
		user = User.objects.get(username=username)
	# Should really never happen, but a failsafe
	except:
		message.error(request, "Something went wrong.")
		dajax.redirect(request.META['HTTP_REFERER'])
		return dajax.json()
	comments = Comment.objects.filter(receiving_user=user).order_by('-date')[:num]
	out = []
	for comment in comments:
		url = '/static/img/user/default'
		pic = UserPicture.objects.filter(user_id=comment.original_poster)
		if pic:
			url = pic[0].pic_link
		out.append("<div class = 'recent-post'><div class = 'post-content'>%s</div><div class = 'post-author'><div class = 'post-author-icon'><img class='poster-img' src='%s'/> </div><div class = 'post-author-title'>%s, %s</div></div></div>" % (comment.comment, url, comment.original_poster.username, comment.date.astimezone(timezone.get_default_timezone()).strftime('%-b %-d %-I:%M %p %Z')))
	if len(Comment.objects.filter(receiving_user=user)) > num:
		out.append("<div class='more-posts' onclick='retrieve_posts(%d);'>More posts</div>" % (num + 5))
	dajax.assign('#recent-posts', 'innerHTML', "".join(out))
	dajax.script('resizeImages();')
	return dajax.json()

@dajaxice_register(method='GET', name='recipe.list_mine')
def list_own_recipes(request, param='name', page=0):
	dajax = Dajax()
	num_per_page = 5
	recipes = Recipe.objects.filter(user_id=request.user).order_by(param)
	count = len(recipes)
	recipes = recipes[page*num_per_page:(page+1)*num_per_page]
	out = []
	if recipes:
		for recipe in recipes:
			out.append("""<div class='recipe-line'>
		  				<div class='recipe-link'>
		    			<a href='/recipe/edit?rid=%d'>%s</a>
		  				</div>
		  				<div class='recipe-line-info'>
		    			<div class='last-edited'>Last edited: %s ago</div><div class='upvotes'>Upvotes: %d</div>
		  				</div>
		  				<div class='created'>Created: %s ago</div>
		  				<hr></div>""" % (recipe.id, recipe.name, timesince(recipe.last_edited), recipe.upvotes, timesince(recipe.added)))
		out.append('<div id = "il-previous-next">');
		if page != 0:
			out.append('<div id = "il-previous" class = "prev clickable" onclick="load_my_recipes(&apos;%s&apos;, %d)"><i class = "fa fa-chevron-left"></i></div>' % (param, page-1))
		else:
			out.append('<div id = "il-previous" class = "prev"><i class = "fa fa-chevron-left"></i></div>')
		if page != count/num_per_page:
			out.append('<div id = "il-next" class = "next clickable" onclick="load_my_recipes(&apos;%s&apos;, %d)"><i class = "fa fa-chevron-right"></i></div>' % (param, page+1))
		else:
			out.append('<div id = "il-next" class = "next"><i class = "fa fa-chevron-right"></i></div>')
		out.append('</div>')
	else:
		out.append("""<div id='recipe-line'>
    			You don't have any recipes - go and make some!
    			</div>""")
	dajax.assign('#recipe-list-container', 'innerHTML', "".join(out))
	return dajax.json()

@dajaxice_register(method='GET', name='recipe.list_all')
def list_all_recipes(request, param='name', username=None, page=0):
	dajax = Dajax()
	out = []
	num_per_page = 5
	recipes = Recipe.objects.all()
	if username and username != '':
		recipes = recipes.filter(user_id__username=username)
	recipes = recipes.filter(public=True).order_by(param)
	count = len(recipes)
	recipes = recipes[page*num_per_page:(page+1)*num_per_page]
	if recipes:
		for recipe in recipes:
			out.append("""<div class='public-recipe-line'>
		  				<div class='public-recipe-link'>
		    			<a href='/recipe/%d'>%s</a>
		  				</div>
		  				<div class='public-recipe-line-info'>
		  				<div class='public-recipe-author'>by %s</div>
		    			<div class='public-upvotes'>Upvotes: %d</div><div class='public-last-edited'>Last edited: %s ago</div>
		  				</div>
		  				<hr></div>""" % (recipe.id, recipe.name, recipe.user_id.username, recipe.upvotes, timesince(recipe.last_edited)))
		out.append('<div id = "il-previous-next">');
		if page != 0:
			out.append('<div id = "il-previous" class = "prev clickable" onclick="load_recipes(&apos;%s&apos;, %d)"><i class = "fa fa-chevron-left"></i></div>' % (param, page-1))
		else:
			out.append('<div id = "il-previous" class = "prev"><i class = "fa fa-chevron-left"></i></div>')
		if page != count/num_per_page:
			out.append('<div id = "il-next" class = "next clickable" onclick="load_recipes(&apos;%s&apos;, %d)"><i class = "fa fa-chevron-right"></i></div>' % (param, page+1))
		else:
			out.append('<div id = "il-next" class = "next"><i class = "fa fa-chevron-right"></i></div>')
		out.append('</div>')
	else:
		out.append("""<div class='public-recipe-line'>
    			No recipes here!
    			</div>""")
	dajax.assign('#public-recipe-list-container', 'innerHTML', "".join(out))
	return dajax.json()
