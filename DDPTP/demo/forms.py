from django import forms

class Submission_form(forms.Form):
    WORKCLASS_CHOICES = (('Private', 'Private'),('Self-emp-not-inc', 'Self-emp-not-inc'),('Self-emp-inc', 'Self-emp-inc'),('Federal-gov', 'Federal-gov'), ('Local-gov', 'Local-gov'), ('State-gov', 'State-gov'), ('Without-pay', 'Without-pay'), ('Never-worked', 'Never-worked'))
    EDUCATION_CHOICES = (('Bachelors', 'Bachelors'), ('Some-college', 'Some-college'), ('11th', '11th'), ('HS-grad', 'HS-grad'), ('Prof-school', 'Prof-school'), ('Assoc-acdm', 'Assoc-acdm'), ('Assoc-voc', 'Assoc-voc'), ('9th', '9th'), ('7th-8th', '7th-8th'), ('12th', '12th'), ('Masters', 'Masters'), ('1st-4th', '1st-4th'), ('10th', '10th'), ('Doctorate', 'Doctorate'), ('5th-6th', '5th-6th'), ('Preschool', 'Preschool'))
    MARITAL_STATUS_CHOICES = (('Married-civ-spouse', 'Married-civ-spouse'), ('Divorced', 'Divorced'), ('Never-married', 'Never-married'), ('Separated', 'Separated'), ('Widowed', 'Widowed'), ('Married-spouse-absent', 'Married-spouse-absent'), ('Married-AF-spouse', 'Married-AF-spouse')) 
    OCCUPATION_CHOICES = (
        ('Tech-support', 'Tech-support'), ('Craft-repair', 'Craft-repair'), ('Other-service', 'Other-service'), ('Sales', 'Sales'), ('Exec-managerial', 'Exec-managerial'), ('Prof-specialty', 'Prof-specialty'), ('Handlers-cleaners', 'Handlers-cleaners'), ('Machine-op-inspct', 'Machine-op-inspct'), ('Adm-clerical', 'Adm-clerical'), ('Farming-fishing', 'Farming-fishing'), 
        ('Transport-moving', 'Transport-moving'), ('Priv-house-serv', 'Priv-house-serv'), ('Protective-serv', 'Protective-serv'), ('Armed-Forces', 'Armed-Forces')
    )
    RELATIONSHIP_CHOICES = (('Wife', 'Wife'), ('Own-child', 'Own-child'), ('Husband', 'Husband'), ('Not-in-family', 'Not-in-family'), ('Other-relative', 'Other-relative'), ('Unmarried', 'Unmarried'))
    RACE_CHOICES = (('White', 'White'), ('Asian-Pac-Islander', 'Asian-Pac-Islander'), ('Amer-Indian-Eskimo', 'Amer-Indian-Eskimo'), ('Other', 'Other'), ('Black', 'Black'))
    SEX_CHOICES = (('Female', 'Female'), ('Male', 'Male'))
    NATIVE_COUNTRY_CHOICES = (
        ('United-States', 'United-States'), ('Cambodia', 'Cambodia'), ('England', 'England'), ('Puerto-Rico', 'Puerto-Rico'), ('Canada', 'Canada'), ('Germany', 'Germany'), ('Outlying-US(Guam-USVI-etc)', 'Outlying-US(Guam-USVI-etc)'), 
        ('India', 'India'), ('Japan', 'Japan'), ('Greece', 'Greece'), ('South', 'South'), ('China', 'China'), ('Cuba', 'Cuba'), ('Iran', 'Iran'), ('Honduras', 'Honduras'), ('Philippines', 'Philippines'), ('Italy', 'Italy'), ('Poland', 'Poland'), 
        ('Jamaica', 'Jamaica'), ('Vietnam', 'Vietnam'), ('Mexico', 'Mexico'), ('Portugal', 'Portugal'), ('Ireland', 'Ireland'), ('France', 'France'), ('Dominican-Republic', 'Dominican-Republic'), ('Laos', 'Laos'), ('Ecuador', 'Ecuador'), ('Taiwan', 'Taiwan'), 
        ('Haiti', 'Haiti'), ('Columbia', 'Columbia'), ('Hungary', 'Hungary'), ('Guatemala', 'Guatemala'), ('Nicaragua', 'Guatemala'), ('Scotland', 'Scotland'), ('Thailand', 'Thailand'), ('Yugoslavia', 'Yugoslavia'), ('El-Salvador', 'El-Salvador'), 
        ('Trinadad&Tobago', 'Trinadad&Tobago'), ('Peru', 'Peru'), ('Hong', 'Hong'), ('Holand-Netherlands', 'Holand-Netherlands')
    )

    age = forms.IntegerField()
    workclass = forms.ChoiceField(choices=WORKCLASS_CHOICES)
    fnlwgt = forms.IntegerField()
    education = forms.ChoiceField(choices=EDUCATION_CHOICES)
    education_num = forms.IntegerField()
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS_CHOICES, widget=forms.Select(attrs={"class": "protected"}))
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES)
    relationship = forms.ChoiceField(choices= RELATIONSHIP_CHOICES)
    race = forms.ChoiceField(choices=RACE_CHOICES ,widget=forms.Select(attrs={"class": "protected"}))
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select(attrs={"class": "protected"}))
    capital_gain = forms.IntegerField()
    capital_loss = forms.IntegerField()
    hours_per_week = forms.IntegerField()
    native_country = forms.ChoiceField(choices=NATIVE_COUNTRY_CHOICES)
    