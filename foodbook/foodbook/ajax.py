from dajax.core import Dajax
import json, decimal
from foodbook.models import Ingredient, ServingSize, Recipe, UserDiet, Comment
from dajaxice.decorators import dajaxice_register
from recipe_utils import calculate_nutritional_value, decimal_json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

@dajaxice_register(method='GET', name='ingredient.update')
def update_search(request, div_id, search, search_type="All"):
	dajax = Dajax()
	if search_type != "All":
		ingredients = Ingredient.objects.filter(name__icontains=search, ingredient_type__name__iexact=search_type)
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
	if search_type != "All":
		ingredients = Ingredient.objects.filter(name__icontains=search, ingredient_type__name__iexact=search_type)
	else:
		ingredients = Ingredient.objects.filter(name__icontains=search)
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
		out.append('<div id = "il-previous" class = "prev" onclick="update_page(%d)"><i class = "fa fa-chevron-left"></i></div>' % (page-1))
	if page != count/num_per_page:
		out.append('<div id = "il-next" class = "next clickable" onclick="update_page(%d)"><i class = "fa fa-chevron-right"></i></div>' % (page+1))
	else:
		out.append('<div id = "il-next" class = "next" onclick="update_page(%d)"><i class = "fa fa-chevron-right"></i></div>' % (page+1))

	out.append('</div>')

	dajax.assign('#' + div_id, 'innerHTML', "".join(out))
	return dajax.json()

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
def save_recipe(request, rid, ingredients, name, description, instructions, ss):
	if request.user.is_authenticated():
		if rid:
			try:
				recipe = Recipe.objects.get(id=rid, user_id=request.user)
			except:
				return json.dumps({'success': False})
			if recipe:
				recipe.name = name
				recipe.description = description
				recipe.servings = ss
				recipe.instructions = instructions
				recipe.ingredients = json.dumps(ingredients)
				recipe.save()
		else:
			recipe = Recipe(name=name, servings = ss, description=description, instructions=instructions, ingredients=json.dumps(ingredients), upvotes=0)
			recipe.save()
			rid = recipe.id
			recipe.user_id.add(request.user)
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
		out.append("<div class = 'recent-post'><div class = 'post-content'>%s</div><div class = 'post-author'><div class = 'post-author-icon'> </div><div class = 'post-author-title'>%s, %s</div></div></div>" % (comment.comment, comment.original_poster.username, comment.date.astimezone(timezone.get_default_timezone()).strftime('%-b %-d %-I:%M %p %Z')))
	dajax.assign('#recent-posts', 'innerHTML', "".join(out))
	return dajax.json()

