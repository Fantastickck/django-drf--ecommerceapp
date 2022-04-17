from django import forms

from .models import Order, OrderItem


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Эл. почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))

