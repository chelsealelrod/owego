from django.db import models
from .category import Category
from django.db.models.deletion import CASCADE


class Bill (models.Model):
    owegouser = models.ForeignKey("owegoapi.owegouser",
            on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=CASCADE,
                                 related_name='category')
    due_date = models.DateField()
    amount_due = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    