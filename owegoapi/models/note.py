from django.db import models
from .bill import Bill


class Note(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,
                             related_name="notes", null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    