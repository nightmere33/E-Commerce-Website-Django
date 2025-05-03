from django.db import models
from item.models import Item
from django.contrib.auth.models import User

class Conversation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='conversations') # ForeignKey to Item model and related_name for reverse lookup and cascade delete
    members = models.ManyToManyField(User , related_name='conversations') # ManyToManyField to User model and related_name for reverse lookup
    created_at = models.DateTimeField(auto_now_add=True) # DateTimeField for created_at with auto_now_add to set the field to now when the object is first created
    modefied_at = models.DateTimeField(auto_now=True) # DateTimeField for modified_at with auto_now to set the field to now every time the object is saved

    class Meta:
        ordering = ('-modefied_at',)


class ConversationMessage(models.Model):
    conversation =  models.ForeignKey(Conversation , related_name='messages' , on_delete=models.CASCADE) # ForeignKey to Conversation model and related_name for reverse lookup and cascade delete
    content = models.TextField() # TextField for content of the message
    created_at = models.DateTimeField(auto_now_add=True) # DateTimeField for created_at with auto_now_add to set the field to now when the object is first created
    created_by = models.ForeignKey(User ,related_name='created_messages', on_delete=models.CASCADE) # ForeignKey to User model and cascade delete
