from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from forms import UserLoginForm, SearchBar, UserCreationForm, ProfilePictureForm, Settings
from django.contrib.auth.decorators import login_required
from foodbook.models import Ingredient, UserDiet, IngredientType, ServingSize, Recipe, IngredientWrapper, UserPicture
import json
from django.http import HttpResponse, HttpResponseRedirect
from user import upload_picture
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.template.defaultfilters import striptags

def home(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

def login_user(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		form.is_valid()
		if 'username' in form.cleaned_data and 'password' in form.cleaned_data:
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				messages.success(request, 'You have successfully logged in.')
			else:
				messages.error(request, 'Username/password combination was incorrect.')
		else:
			messages.error(request, 'Improper username/password.')
		if 'HTTP_REFERER' in request.META:
			return redirect(request.META['HTTP_REFERER'])
		else:
			return redirect('/home')
	return redirect('/home')

def register_view(request):
	if request.user.is_authenticated():
		return redirect('/home')
	form = UserCreationForm()
	return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

def register(request):
	if request.user.is_authenticated():
		return redirect('/home')
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			if len(User.objects.filter(username=form.cleaned_data['username'])) > 0:
				messages.error(request, "This username has already been taken.")
			elif len(User.objects.filter(email=form.cleaned_data['email'])) > 0:
				messages.error(request, "This email is already tied to an account.")
			else:
				new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
				messages.success(request, 'Registration was successful. You can now log in to your account.')
		else:
			if form['username'].errors or form['password'].errors or form['email'].errors:
				messages.error(request, "All fields are required.")
			elif form.non_field_errors():
				messages.error(request, striptags(form.non_field_errors()))
	return redirect('/register')

def logout_user(request):
	if request.user.is_authenticated():
		messages.success(request, "You have successfully logged out.")
		logout(request)
	return HttpResponseRedirect('/home')

def default_page(request):
	return render_to_response('404.html', context_instance=RequestContext(request))

def show_ingredient(request, ingredient):
	ingredient = Ingredient.objects.filter(name__iexact=ingredient)
	if ingredient:
		ingredient = ingredient.values()[0]
	return render_to_response('ingredient.html', {'ingredient': ingredient})

def search_ingredients(request):
	if request.method == 'POST':
		form = SearchBar(request.POST)
		search = True
		if form.is_valid():
			manager = Ingredient.objects.filter(name__startswith=form.cleaned_data['searchbar']).order_by('name')
	else:
		form = SearchBar()
		search = False
		manager = Ingredient.objects.all()
	return render_to_response('search_ingredients.html', {'form': form, 'ingredient_list': manager, 'search': search}, context_instance=RequestContext(request))

def add_recipe(request):
	ingredient_list = []
	recipe = None
	if request.user.is_authenticated() and request.method == 'GET' and 'rid' in request.GET:
		recipe = request.GET['rid']
		try:
			recipe = Recipe.objects.get(id=recipe, user_id=request.user)
		except:
			messages.error(request, "Invalid recipe.")
			return redirect('/recipe')
		ingredients = json.loads(recipe.ingredients_text)
		for i in xrange(len(ingredients['id'])):
			ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
	i_types = [('Meat', 'meat'), ('Fruits', 'fruits'), ('Grains', 'grains'), ('Seafood', 'seafood'), ('Nuts and Legumes', 'nuts-and-legumes'), ('Soups and Sauces', 'soups-and-sauces'), ('Spices and Herbs', 'spices-and-herbs'), ('Vegetables', 'vegetables'), ('Fats and Oils', 'fats-and-oils'), ('Dairy and Eggs', 'dairy-and-eggs')]
	if request.user.is_authenticated():
		return render_to_response('add_recipe.html', {'type_list': i_types, 'ingredient_list': ingredient_list, 'recipe': recipe}, context_instance=RequestContext(request))
	else:
		messages.error(request, "You must log in to add recipes.")
		return redirect('/recipe')

def list_my_recipes(request):
	my_recipes = None
	my_diet = None
	if request.user.is_authenticated():
		my_recipes = Recipe.objects.filter(user_id=request.user)
		try:
			my_diet = UserDiet.objects.get(user=request.user)
		except:
			my_diet = None
	return render_to_response('view_recipe.html', {'recipes': my_recipes, 'diet': my_diet}, context_instance=RequestContext(request))


def display_user_profile(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			upload_picture(request)
			return redirect('/user')
		else:
			form = ProfilePictureForm()
			url = '/static/img/user/default'
			pic = UserPicture.objects.filter(user_id=request.user)
			if pic:
				url = pic[0].pic_link
			return render_to_response('user_page.html', {'form': form, 'is_me': True, 'user':request.user, 'users':request.user, 'profile_picture': url, 'recipe_count': len(request.user.recipe_set.filter(public=True)), 'reputation': sum([recipe.upvotes for recipe in request.user.recipe_set.filter(public=True)])}, context_instance = RequestContext(request))
	return redirect('/home')

def display_other_profile(request, user):
	try:
		user = User.objects.get(username=user)
	except Exception, e:
		messages.error(request, "That user doesn't exist.")
		return redirect('/home')
	url = '/static/img/user/default'
	if user:
		pic = UserPicture.objects.filter(user_id=user)
		if pic:
			url = pic[0].pic_link
	return render_to_response('user_page.html', {'users': user, 'recipe_count': len(user.recipe_set.filter(public=True)), 'is_me': False, 'profile_picture': url, 'reputation': sum([recipe.upvotes for recipe in user.recipe_set.filter(public=True)])}, context_instance=RequestContext(request))

def display_user_settings(request):
	if request.user.is_authenticated():
		try:
			diet = UserDiet.objects.get(user=request.user)
		except:
			diet = None
		return render_to_response('user_settings.html', {'diet': diet}, context_instance = RequestContext(request))
	return redirect('/home')

def display_normal_recipe(request, rid):
	ingredient_list = []
	try:
		recipe = Recipe.objects.get(id=rid)
		ingredients = json.loads(recipe.ingredients_text)
		for i in xrange(len(ingredients['id'])):
			ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
	except:
		messages.error(request, "That recipe doesn't exist.")
		if 'HTTP_REFERER' in request.META:
			return redirect(request.META['HTTP_REFERER'])
		else:
			return redirect('/recipe')
	return render_to_response('recipe_page.html', {'recipe': recipe, 'ingredient_list': ingredient_list}, context_instance = RequestContext(request))

def save_settings(request):
	if request.user.is_authenticated() and request.method == 'POST':
		form = Settings(request.POST)
		form.is_valid()
		if 'old_password' in form.cleaned_data:
			if not check_password(form.cleaned_data['old_password'],request.user.password):
				messages.error(request, "Incorrect password.")
				return redirect('/settings')
			if form.cleaned_data['new_password'] == form.cleaned_data['new_password_confirm']:
				request.user.set_password(form.cleaned_data['new_password'])
				request.user.save()
				messages.success(request, "Save successful.")
				return redirect('/settings')
			else:
				messages.error(request, "Your new passwords did not match.")
				return redirect('/settings')
		if form['fat'].errors or form['calories'].errors or form['protein'].errors or form['carbs'].errors:
			messages.error(request, "Diet parameters must be integers.")
			return redirect('/settings')
		try:
			diet = UserDiet.objects.get(user=request.user)
			diet.halal = form.cleaned_data['halal']
			diet.lacto = form.cleaned_data['lacto']
			diet.lactoovo = form.cleaned_data['lactoovo']
			diet.vegan = form.cleaned_data['vegan']
			diet.diabetes = form.cleaned_data['diabetes']
			diet.hypertension = form.cleaned_data['hypertension']
			diet.nuts = form.cleaned_data['nuts']
			diet.lactose = form.cleaned_data['lactose']
			diet.eggs = form.cleaned_data['eggs']
			diet.soy = form.cleaned_data['soy']
			diet.shellfish = form.cleaned_data['shellfish']
			diet.fish = form.cleaned_data['fish']
		except:
			diet = UserDiet(user=request.user, halal=form.cleaned_data['halal'], lacto=form.cleaned_data['lacto'],
				lactoovo=form.cleaned_data['lactoovo'], vegan=form.cleaned_data['vegan'], diabetes=form.cleaned_data['diabetes'],
				hypertension=form.cleaned_data['hypertension'], nuts=form.cleaned_data['nuts'], lactose=form.cleaned_data['lactose'],
				eggs=form.cleaned_data['eggs'], soy=form.cleaned_data['soy'], shellfish=form.cleaned_data['shellfish'], fish=form.cleaned_data['fish'])
		diet.calories = form.cleaned_data['calories']
		diet.fat = form.cleaned_data['fat']
		diet.sugar = form.cleaned_data['carbs']
		diet.protein = form.cleaned_data['protein']
		diet.save()
		messages.success(request, "Save successful.")
		return redirect('/settings')
	return redirect('/home')

def json_database(request):
    search = User.objects.filter(username__istartswith=request.GET['term'])
    results = []
    for r in search:
        results.append(r.username)
    resp = json.dumps(results)
    return HttpResponse(resp, content_type='application/json')


############################## CONTEXT PROCESSORS
def login_processor(request):
	# Makes sure the login form is always given to a page
	return {
		'LOGIN_FORM': UserLoginForm()
	}

def user_profile(request):
	url = '/static/img/user/default'
	if request.user.is_authenticated():
		pic = UserPicture.objects.filter(user_id=request.user)
		if pic:
			url = pic[0].pic_link
	return {
		'PROFILE_PICTURE': url
	}