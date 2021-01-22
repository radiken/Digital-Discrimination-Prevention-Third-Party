from django.db import models

# Create your models here.
class adult_original(models.Model):
    age = models.IntegerField()
    name = models.CharField()
    fnlwgt = models.IntegerField()
    education = models.CharField()
    education_num = models.IntegerField()
    marital_status = models.CharField()
    occupation = models.CharField()
    relationship = models.CharField()
    race = models.CharField()
    sex = models.CharField()
    capital_gain = models.IntegerField()
    capital_loss = models.IntegerField()
    hours_per_week = models.IntegerField()
    native_country = models.CharField()
    income = models.CharField()