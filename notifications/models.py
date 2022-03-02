from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='recipient')
    subject = models.CharField(max_length=100)
    body = RichTextField(blank=True, null=True)
    read = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)