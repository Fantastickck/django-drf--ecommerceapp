from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Эл. почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))


RATING = [(i, str(i)) for i in range(1, 6)] #Неправильная реализация!!!

class FeedbackForm(forms.Form):
    text = forms.CharField(label='Текст отзыва', widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    rating = forms.TypedChoiceField(choices=RATING, coerce=int, label='Оценка')