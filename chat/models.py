from django.db import models
from django.conf import settings

# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="conversation")
    title = models.CharField(max_length=255,default="New chat")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}-{self.user}"

class Message(models.Model):
    SENDER_CHOICES = (
        ("user", "User"),
        ("ai", "AI"),
    )
    sender = models.CharField(max_length=10,choices=SENDER_CHOICES,default='user')
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages")
    content = models.TextField(default=" ")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}:{self.content[:30]}"
    
