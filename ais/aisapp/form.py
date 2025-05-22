from django import forms
from . models import Form, Report

class productForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['user', 'raw_material', 'quantity', 'description']
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'content', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-text-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
        }