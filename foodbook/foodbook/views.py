from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm

def showHome(request):
	return render_to_response('index.html', {})

def test_login(request):
	message = ''
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					message = 'You have logged in as: ' + username
				else:
					message = 'Disabled account'
			else:
				message = "Failed login"
	else:
		form = UserLoginForm()
	return render_to_response('index.html', {'message': message, 'form': form}, context_instance=RequestContext(request))

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

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
	email = forms.CharField(widget=forms.EmailInput)