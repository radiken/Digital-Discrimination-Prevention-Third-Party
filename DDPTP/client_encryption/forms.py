from django import forms

from .models import Individual

class Individual_creation_form(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['title', 'name', 'gender', 'age']

class Submission_form(forms.Form):
    title = forms.CharField()
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your name", "class": "name"}))
    gender = forms.CharField()
    age = forms.DecimalField()