from django.db import models

class Category(models.model):
    label = models.CharField(max_length=50)