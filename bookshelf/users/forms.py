from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:

        model = User
        fields = ("username","email","password1","password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con este correo electrónico"
            )

        return email

class UsernameChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']