from django import forms

class MessageForm(forms.Form): 
    text = forms.CharField(label='Текст сообщения', widget=forms.TextInput(attrs={'class': 'form-control'}))
