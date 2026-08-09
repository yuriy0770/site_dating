from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2', 'email', 'phone']