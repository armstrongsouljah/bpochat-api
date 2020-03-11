from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
    message_text = models.TextField()
    receipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receipient}"

    class Meta:
        ordering = ['-date_sent']

