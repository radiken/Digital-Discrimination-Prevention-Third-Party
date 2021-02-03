from django import forms

class Submission_form(forms.Form):
    age = forms.IntegerField()
    workclass = forms.CharField(max_length = 30)
    fnlwgt = forms.IntegerField()
    education = forms.CharField(max_length = 30)
    education_num = forms.IntegerField()
    marital_status = forms.CharField(widget=forms.TextInput(attrs={"class": "protected"}))
    occupation = forms.CharField(max_length = 30)
    relationship = forms.CharField(max_length = 30)
    race = forms.CharField(widget=forms.TextInput(attrs={"class": "protected"}))
    sex = forms.CharField(widget=forms.TextInput(attrs={"class": "protected"}))
    capital_gain = forms.IntegerField()
    capital_loss = forms.IntegerField()
    hours_per_week = forms.IntegerField()
    native_country = forms.CharField(max_length = 30)
    income = forms.CharField(max_length = 30)