from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Thread(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sendr')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recv')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']