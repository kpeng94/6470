from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def showHome(request):
	return render_to_response('index.html', {})

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
	return render_to_response('index.html', {'message': message, 'form': form, 'not_logged_in': not_logged_in, 'user': request.user}, context_instance=RequestContext(request))

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
			new_user = form.save()
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

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
	email = forms.CharField(widget=forms.EmailInput)