from django import forms
from . models import Form

class productForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['user', 'product_name', 'quantity', 'description']