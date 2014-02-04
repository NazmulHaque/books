from django import forms
from models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user', 'thumbnail', 'created_at']