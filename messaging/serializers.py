from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_text', 'sender', 'receipient' )
    
    def create(self, validated_data):
        return Message.objects.create(**validated_data)
