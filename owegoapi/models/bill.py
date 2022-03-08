from django.db import models
from .category import Category
from .note import Note
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
User = get_user_model()


class Bill (models.model):
    
    user = models.OneToOneField(User,
          on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=CASCADE, related_name='tags')
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name='category')
    due_date = models
    amount_due = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    