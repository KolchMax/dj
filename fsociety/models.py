from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    text = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text
