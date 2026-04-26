from django.db import models
from django.conf import settings

# Create your models here.
class conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="conversation")
    title = models.CharField(max_length=255,default="New chat")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}-{self.user}"
