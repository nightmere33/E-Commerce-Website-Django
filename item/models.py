from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)  # <-- lowercase 'ordering'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    Category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', null=True, blank=True)  # Made nullable again
    carousel_image = models.ImageField(upload_to='carousel_images', null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name