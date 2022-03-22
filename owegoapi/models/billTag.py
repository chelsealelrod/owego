from django.db import models
from .tag import Tag



class BillTag(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="Tag", null=True,
        on_delete=models.SET_NULL)
    