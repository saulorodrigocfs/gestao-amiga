from django.contribut.auth.forms import UserCreationForm, AuthenticationForm
from django.contribut.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        