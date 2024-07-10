from django import forms
from .models import Link

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ('name', 'url')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Guarda tu link con un nombre (Opcional)'}),
            'url': forms.URLInput(attrs={'class': 'form-control text-center', 'placeholder': 'Ingresa una URL'}),
        }
        labels = {
            'url': ''
        }