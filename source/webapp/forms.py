from django import forms
from .models import (Product, Category, Review)
from django.contrib.auth import get_user_model
class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        category = forms.ModelChoiceField(queryset=Category.objects.all())
        fields = ('name','description', 'category', 'picture')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review', 'rating')

class ModerateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('is_moderated',)

