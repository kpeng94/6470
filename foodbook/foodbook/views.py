from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from forms import UserLoginForm, SearchBar, UserCreationForm
from django.contrib.auth.decorators import login_required
from foodbook.models import Ingredient, IngredientType, ServingSize, Recipe
import json
from django.http import HttpResponse

class IngredientWrapper():
	def __init__(self, iid, quantity, measurement, iname):
		self.ingredient_id = iid
		self.qty = quantity
		self.unit = measurement
		self.name = iname
		self.servingsize = Ingredient.objects.get(id=iid).servingsize_set.all()

def showHome(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

def test_login(request):
	message = ''
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			message = login_user(request)
	else:
		form = UserLoginForm()
	if request.user.is_authenticated():
		not_logged_in = False
	else:
		not_logged_in = True
	return render_to_response('index.html', {'message': message, 'form': form}, context_instance=RequestContext(request))

def login_user(request):
	form = UserLoginForm(request.POST)
	form.is_valid()
	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request,user)
		return 'You have logged in as ' + username + '.'
	else:
		return 'Your username/password combination was not correct.'

def register(request):
	message = ''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
			message = 'Registration successful!'
	else:
		form = UserCreationForm()
	return render_to_response('register.html', {'message': message, 'form': form}, context_instance=RequestContext(request))

def logout_user(request):
	if request.user.is_authenticated():
		logout(request)
	return redirect('/home')

def default_page(request):
	if not request.user.is_authenticated():
		return redirect('/home')
	return render_to_response('default.html', {'username': request.user.username})

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
	recipe_id =  ''
	if request.user.is_authenticated() and request.method == 'GET' and 'rid' in request.GET:
		recipe_id = request.GET['rid']
		try:
			recipe = Recipe.objects.get(id=recipe_id, user_id=request.user)
		except:
			return HttpResponse("This isn't your recipe, or this recipe doesn't exist.")
		else:
			ingredients = json.loads(recipe.ingredients)
			for i in xrange(len(ingredients['id'])):
				ingredient_name = Ingredient.objects.get(id=ingredients['id'][i]).name
				ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i], ingredient_name))
	ingredient_types = IngredientType.objects.all()
	i_types = [types.name for types in ingredient_types]
	return render_to_response('add_recipe.html', {'type_list': i_types, 'ingredient_list': ingredient_list, 'recipe_id': recipe_id}, context_instance=RequestContext(request))

def list_my_recipes(request):
	if request.user.is_authenticated():
		my_recipes = Recipe.objects.filter(user_id=request.user)
		return render_to_response('view_recipe.html', {'recipes': my_recipes}, context_instance=RequestContext(request))
	else:
		return HttpResponse("Log in to see your recipes.")

############################## CONTEXT PROCESSORS
def login_processor(request):
	# Makes sure the login form is always given to a page
	return {
		'LOGIN_FORM': UserLoginForm()
	}