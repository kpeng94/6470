from django import forms

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class SearchBar(forms.Form):
	searchbar = forms.CharField(max_length=100)