from django.shortcuts import render
from rest_framework import generics as g
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    IndividualChatSerializer,
)
from .models import IndividualChat


class DirectMessageView(g.ListCreateAPIView):
    serializer_class = IndividualChatSerializer
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self, *args, **kwargs):
        username = kwargs.get('username')
        current_user = self.request.user
        qs = IndividualChat.objects.filter(to__username__iexact=username, sender=current_user)
        return qs

    def post(self, reqest, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data)
        serializer.is_valid(raizes_exception=True)
        return Response(data = serializer.data, status=status.HTTP_201_CREATED)