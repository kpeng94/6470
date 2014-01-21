from django import forms

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

		if password and pw_confirm:
			if password != pw_confirm:
				raise forms.ValidationError(u'Your passwords must be the same.')

		return cleaned_data

class ProfilePictureForm(forms.Form):
	image = forms.ImageField()