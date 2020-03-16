from django.shortcuts import render, get_object_or_404
from rest_framework import generics as g
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    IndividualChatSerializer,
)
from django.contrib.auth import get_user_model
from .models import IndividualChat


User = get_user_model()


class DirectMessageView(g.CreateAPIView):
    serializer_class = IndividualChatSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return IndividualChat.objects.all()

    def post(self, request, *args, **kwargs):
        receipient = get_object_or_404(User, username=kwargs.get("username")).pk
        sender =request.user.pk
        user_data = {
          "message": request.data.get("message"),
          "to": receipient,
          "sender": sender
        }
        if receipient == sender:
            error_msg = "Cannot send a message to yourself"
            return Response(data= error_msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_message = {
            "success": "message sent successfully"
        }
        return Response(data=response_message, status=status.HTTP_201_CREATED)