from django import forms
from . models import Form, Report

class productForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['user', 'raw_material', 'quantity', 'description']
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'content']