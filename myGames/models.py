# models.py

from django.db import models
from django.contrib.auth.models import User
from item.models import Item  

class MyGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_games')
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey('payment.Order', on_delete=models.CASCADE)
    key = models.CharField(max_length=255)  # to store the generated key
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
