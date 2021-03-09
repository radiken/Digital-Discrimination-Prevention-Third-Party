from django import forms

class Adult_submission_form(forms.Form):
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
    
class Statlog_submission_form(forms.Form):
    ACCOUNT_STATUS_CHOICES = (('A11', 'Less than 0 DM'),('A12', '0 to 200 DM'),('A13', 'Greater than 200 DM'),('A14', 'No checking account'))
    CREDIT_HISTORY_CHOICES = (('A30', 'no credits taken/all credits paid back duly'), ('A31', 'all credits at this bank paid back duly'), ('A32', 'existing credits paid back duly till now'), ('A33', 'delay in paying off in the past'), ('A34', 'critical account/other credits existing (not at this bank)'))
    PURPOSE_CHOICES = (('A40', 'car (new)'), ('A41', 'car (used)'), ('A42', 'furniture/equipment'), ('A43', 'radio/television'), ('A44', 'domestic appliances'), ('A45', 'repairs'), ('A46', 'education'), ('A48', 'retraining'), ('A49', 'business'), ('A410', 'others0'))
    SAVING_ACCOUNT_CHOICES = (('A61', 'Less than 100 DM'), ('A62', '100 to 500 DM'), ('A63', '500 to 1000 DM'), ('A64', 'greater than 1000 DM'), ('A65', 'unknown / no saving account'))
    PRESENT_EMPLOYMENT_SINCE_CHOICES = (('A71', 'unemployed'), ('A72', 'Less than 1 year'), ('A73', '1 to 4 years'), ('A74', '4 to 7 years'), ('A75', 'more than 7 years'))
    PERSONAL_STATUS_AND_SEX_CHOICES = (('A91', 'Male, divorced/separated'), ('A92', 'Female, divorced/separated/married'), ('A93', 'Male, single'), ('A94', 'Male, married/widowed'), ('A95', 'Female, single'))
    GUARANTORS_CHOICES = (('A101', 'None'), ('A102', 'Co-applicant'), ('A103', 'guarantor'))
    PROPERTY_CHOICES = (('A121', 'real estate'), ('A122', 'building society saving agreement / life insurance'), ('A123', 'car or other'), ('A124', 'unknown / no property'))
    OTHER_INSTALLMENT_PLAN_CHOICES = (('A141', 'bank'), ('A142', 'stores'), ('A143', 'none'))
    HOUSING_CHOICES = (('A151', 'rent'), ('A152', 'own'), ('A153', 'for free'))
    JOB_CHOICES = (('A171', 'unemployed/unskilled - non-resident'), ('A172', 'unskilled - resident'), ('A173', 'skill employee / official'), ('A174', 'management/self-employed/highly qualified employee/officer'))
    TELEPHONE_CHOICES = (('A191', 'none'), ('A192', 'yes, registered under the costomers name'))
    FOREIGN_WORKER_CHOICES = (('A201', 'yes'), ('A202', 'no'))

    account_status = forms.ChoiceField(choices = ACCOUNT_STATUS_CHOICES, help_text="Status of existing checking account")
    duration = forms.IntegerField(help_text="Duration in month")
    credit_history = forms.ChoiceField(choices = CREDIT_HISTORY_CHOICES, help_text="")
    purpose = forms.ChoiceField(choices = PURPOSE_CHOICES, help_text="")
    credit_amount = forms.IntegerField(help_text="")
    savings_account = forms.ChoiceField(choices = SAVING_ACCOUNT_CHOICES, help_text="")
    present_employment_since = forms.ChoiceField(choices = PRESENT_EMPLOYMENT_SINCE_CHOICES, help_text="")
    installment_rate_in_income = forms.IntegerField(help_text="Installment rate in percentage of disposable income")
    personal_status_and_sex = forms.ChoiceField(choices = PERSONAL_STATUS_AND_SEX_CHOICES, help_text="")
    guarantors = forms.ChoiceField(choices = GUARANTORS_CHOICES, help_text="")
    present_residence_since = forms.IntegerField(help_text="")
    property = forms.ChoiceField(choices = PROPERTY_CHOICES, help_text="")
    age = forms.IntegerField(help_text="")
    other_installment_plans = forms.ChoiceField(choices = OTHER_INSTALLMENT_PLAN_CHOICES, help_text="")
    housing = forms.ChoiceField(choices = HOUSING_CHOICES, help_text="")
    existing_credits = forms.IntegerField(help_text="Number of existing credits at this bank")
    job = forms.ChoiceField(choices = JOB_CHOICES, help_text="")
    maintenance_provider_number = forms.IntegerField(help_text="Number of people being liable to provide maintenance for")
    telephone = forms.ChoiceField(choices = TELEPHONE_CHOICES, help_text="")
    foreign_worker = forms.ChoiceField(choices = FOREIGN_WORKER_CHOICES, help_text="")
    result = forms.IntegerField(help_text="")