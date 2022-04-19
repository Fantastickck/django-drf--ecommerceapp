from cProfile import label
from math import fabs
from django import forms

RATING = [(i, str(i)) for i in range(1, 6)]

class FeedbackForm(forms.Form):
    text = forms.CharField(label='Текст отзыва', widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    rating = forms.TypedChoiceField(choices=RATING, coerce=int, label='Оценка')
