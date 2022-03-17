from django.db import models
from .bill import Bill

class Tag (models.Model):
    
  label = models.CharField(max_length=50)
  bill_tag = models.ManyToManyField(Bill)