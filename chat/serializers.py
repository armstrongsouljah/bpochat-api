from rest_framework import serializers
from .models import (
    ChatRoom, 
    ChatMessage,
    IndividualChat
)
from authentication.serializers import UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = ChatRoom
        fields = ('creator', 'name', 'members')


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('room', 'message', 'sender', 'sent_at')


class IndividualChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualChat
        fields = '__all__'