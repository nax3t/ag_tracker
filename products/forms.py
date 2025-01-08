from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'quantity', 
            'unit', 'cost_per_unit', 'minimum_stock', 
            'expiry_date', 'supplier', 'location', 'latitude', 'longitude'
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
        }
        help_texts = {
            'location': 'Full location name (e.g., "Central Valley Farm, Fresno, CA")',
            'latitude': 'Decimal degrees (e.g., 36.7378)',
            'longitude': 'Decimal degrees (e.g., -119.7871)',
        } 