from django import forms

from .models import Order, OrderItem


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Имя')
    last_name = forms.CharField(max_length=255, label='Фамилия')
    email = forms.EmailField(label='Эл. почта')
    address = forms.CharField(max_length=255, label='Адрес')

    class Meta:
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

