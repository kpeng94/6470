from django import forms
import re

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class SearchBar(forms.Form):
	searchbar = forms.CharField(max_length=100)

class UserCreationForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	pw_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'E-Mail'}))

	def clean(self):
		cleaned_data = super(UserCreationForm, self).clean()
		pw_confirm = cleaned_data.get("pw_confirm")
		password = cleaned_data.get("password")

		valid = re.match('^[\w]+$', cleaned_data.get("username"))
		if not valid:
			raise forms.ValidationError(u'Your username must only consist of alphanumericals.')
		if password and pw_confirm:
			if password != pw_confirm:
				raise forms.ValidationError(u'Your passwords must be the same.')

		return cleaned_data

class ProfilePictureForm(forms.Form):
	image = forms.ImageField()

class Settings(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput)
	new_password = forms.CharField(widget=forms.PasswordInput)
	new_password_confirm = forms.CharField(widget=forms.PasswordInput)
	halal = forms.BooleanField(required=False)
	lacto = forms.BooleanField(required=False)
	lactoovo = forms.BooleanField(required=False)
	vegan = forms.BooleanField(required=False)
	diabetes = forms.BooleanField(required=False)
	hypertension = forms.BooleanField(required=False)
	nuts = forms.BooleanField(required=False)
	eggs = forms.BooleanField(required=False)
	dairy = forms.BooleanField(required=False)
	shellfish = forms.BooleanField(required=False)
	fish = forms.BooleanField(required=False)
	soy = forms.BooleanField(required=False)
	lactose = forms.BooleanField(required=False)
	calories = forms.IntegerField(required=False)
	fat = forms.IntegerField(required=False)
	protein = forms.IntegerField(required=False)
	carbs = forms.IntegerField(required=False)