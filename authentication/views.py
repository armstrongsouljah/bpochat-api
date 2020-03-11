from django.shortcuts import render
from rest_framework import generics
from .renderers import (
    UserJSONRenderer,
)
from rest_framework.permissions import (
    AllowAny,
)
from .serializers import (
    RegistrationSerializer,
    LoginSerializer
)
from rest_framework.response import Response
from rest_framework import status


class RegistrationView(generics.CreateAPIView):
    """
     This class creates a new user and saves it in the database
    """
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    renderer_classes = [UserJSONRenderer, ]

    def post(self, *args, **kwargs):
        user = self.request.data.get('user', {})
        print('user data', self.request.data)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({'token': serializer.data.get('token')}, status=status.HTTP_200_OK)