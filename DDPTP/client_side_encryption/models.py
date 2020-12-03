from django.db import models

# Create your models here.
class Individuals(models.Model):
	title = models.TextField()
	name = models.TextField()
	gender = models.TextField()
	age = models.TextField()