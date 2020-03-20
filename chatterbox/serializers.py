from rest_framework import serializers
from .models import Thread, Message
from authentication.serializers import UserSerializer

class ThreadSerializer(serializers.ModelSerializer):
    first_user = UserSerializer(read_only=True)
    second_user = UserSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = ('first_user', 'second_user')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    thread = ThreadSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('thread', 'sender', 'message')
