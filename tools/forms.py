from django import forms
from .models import Tool

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['barcode', 'name', 'location', 'category', 'description', 'borrowed_by', 'borrow_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
        }