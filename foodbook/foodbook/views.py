from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from forms import UserLoginForm, SearchBar, UserCreationForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required
from foodbook.models import Ingredient, IngredientType, ServingSize, Recipe, IngredientWrapper, UserPicture
import json
from django.http import HttpResponse, HttpResponseRedirect
from user import upload_picture

def home(request):
	message = ''
	return render_to_response('index.html', {'message': message}, context_instance=RequestContext(request))

def login_user(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		form.is_valid()
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
		return redirect('' + request.META['HTTP_REFERER'])
	return redirect('/home')

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
	return HttpResponseRedirect('/home')

def default_page(request):
	return redirect('/home')

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
			return HttpResponse("This isn't your recipe, or this recipe doesn't exist.")
		else:
			ingredients = json.loads(recipe.ingredients)
			for i in xrange(len(ingredients['id'])):
				ingredient_name = Ingredient.objects.get(id=ingredients['id'][i]).name
				ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
	ingredient_types = IngredientType.objects.all()
	i_types = [types.name for types in ingredient_types]
	return render_to_response('add_recipe.html', {'type_list': i_types, 'ingredient_list': ingredient_list, 'recipe': recipe}, context_instance=RequestContext(request))

def list_my_recipes(request):
	if request.user.is_authenticated():
		my_recipes = Recipe.objects.filter(user_id=request.user)
		return render_to_response('view_recipe.html', {'recipes': my_recipes}, context_instance=RequestContext(request))
	else:
		return HttpResponse("Log in to see your recipes.")

def display_user_profile(request):
	if request.method == 'POST':
		upload_picture(request)
		return redirect('/user')
	if request.user.is_authenticated():
		form = ProfilePictureForm()
		return render_to_response('user_page.html', {'form': form}, context_instance = RequestContext(request))
	return redirect('/home')

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
