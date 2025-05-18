from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' not in username or '.' not in username:
            raise forms.ValidationError("Please enter a valid email address.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This email is already registered.")
        return username