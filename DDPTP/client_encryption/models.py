from django.db import models

# Create your models here.
class Individual(models.Model):
	title = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	gender = models.CharField(max_length=20)
	age = models.DecimalField(decimal_places=0, max_digits=3)