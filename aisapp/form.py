from django import forms
from . models import Form

class productForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['user', 'raw_material', 'quantity', 'description']