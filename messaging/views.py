from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class MessageView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    
    def post(self, request, *args, **kwargs):

        sender = User.objects.get(username=request.user)
        receipient = User.objects.get(username=kwargs.get("username"))
        data = {
            "sender":sender.pk,
            "receipient":receipient.pk,
            "message_text": request.data.get("message_text")
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
