from django import forms
from models import Products

from books import settings


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['user', 'thumbnail', 'created_at', 'money_type', 'updated_at', 'status']

class changeProductPhoto(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['thumbnail']