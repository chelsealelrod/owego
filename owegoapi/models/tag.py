from django.db import models
from .note import Note

class Tag (models.Model):
    
  label = models.CharField(max_length=50)
  note_tag = models.ManyToManyField(Note)