
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from .models import AdvUser, Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=255, label='Имя пользователя', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    date_of_birth = forms.CharField(label='Дата рождения', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    default_address = forms.CharField(label='Адрес по умолчанию', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    # slug = forms.CharField(label='Уникальный инернет-адрес', required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'date_of_birth', 'default_address')
        

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль'}))
    new_password_again = forms.CharField(label='Повтор', widget=forms.PasswordInput(attrs={'placeholder': 'Повтор нового пароля'}))