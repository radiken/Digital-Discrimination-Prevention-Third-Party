from django.db import models

# Create your models here.
class Individual(models.Model):
	title = models.TextField(max_length=50)
	name = models.TextField(max_length=100)
	gender = models.TextField()
	age = models.DecimalField(decimal_places=0, max_digits=100)