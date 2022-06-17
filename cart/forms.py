from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)] # Переделать данную реализацию!!!


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Кол-во')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    