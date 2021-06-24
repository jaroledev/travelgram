"""User forms"""
#Django
from django import forms

#Models
from django.contrib.auth.models import User
from users.models import Profile

class SignupForm(forms.Form):
    """Sign up form"""

    first_name = forms.CharField(
        label=False,
        min_length=3,
        max_length=50,
        widget = forms.TextInput(
            attrs=
            {'placeholder':'Name','class':
            'form-control','required': True}))

    last_name = forms.CharField(
        label=False,
        min_length=3,
        max_length=50,
        widget = forms.TextInput(
            attrs=
            {'placeholder':'Last Name','class':
            'form-control','required': True}))
    
    username = forms.CharField(
        label=False,
        min_length=3,
        max_length=50, 
        widget = forms.TextInput(
            attrs=
            {'placeholder':'Username','class':
            'form-control','required': True}))

    email = forms.EmailField(
        label=False,
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(
            attrs=
            {'placeholder':'Email address','class':
            'form-control','required': True}))
    
    password = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(
            attrs=
            {'placeholder':'Password','class':
            'form-control','required': True}))

    password_confirmation = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(
            attrs=
            {'placeholder':'Confirm your Password','class':
            'form-control','required': True}))

   

    def clean_username(self):
        """Username must be unique"""
        username=self.cleaned_data['username']
        #Utilizamos filter poque si usamos get y no existe lanza una exception
        username_query= User.objects.filter(username=username).exists()
        if username_query:
            raise forms.ValidationError('Username is already in use')
        return username

    def clean(self):
        """ Verify password confirmation match"""
        data=super().clean()
        password=data['password']
        password_confirmation=data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')
        return data
    
    def save(self):
        """Create user and profile"""
        data=self.cleaned_data
        data.pop('password_confirmation')
        user=User.objects.create_user(**data)
        profile=Profile(user=user)
        profile.save()




class ProfileForm(forms.Form):
    """Profile form."""
    website = forms.URLField(max_length=200,required=True)
    biography = forms.CharField(max_length=500,required=False)
    phone_number= forms.CharField(max_length=20, required=False)
    picture=forms.ImageField()