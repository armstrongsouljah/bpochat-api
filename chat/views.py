from django.shortcuts import render, get_object_or_404
from rest_framework import generics as g
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    IndividualChatSerializer,
    ChatRoomSerializer
)
from django.contrib.auth import get_user_model
from .models import IndividualChat, ChatRoom


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


class ChatroomView(g.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated, )

    queryset = ChatRoom.objects.all()

    def post(self, request, *args, **kwargs):
        """ allows the user to create a chat room """
        grp_creator = request.user.pk
        grp_name = request.data.get("name")
        request_data = {
            "name": grp_name,
            "creator": grp_creator
        }
        qs = self.queryset.filter(name=grp_name)
        if qs.count() >=1:
            return Response(data={"message": "Group already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = {"message":"Group successfully created"}
        return Response(data=resp, status=status.HTTP_201_CREATED)


class GroupJoinView(g.UpdateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        group = get_object_or_404(ChatRoom, name=kwargs.get("name"))
        user_in_group = group.members.filter(chatroom__members__username=request.user)
        if not len(user_in_group):
            group.members.add(request.user.pk)
            return Response(data="Successfully joined the group", status=status.HTTP_202_ACCEPTED)
        return Response(data="You already  are a member of the group", status=status.HTTP_202_ACCEPTED)
        
        

class GroupLeaveView(g.UpdateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        group = get_object_or_404(ChatRoom, name=kwargs.get("name"))
        user_in_group = group.members.filter(chatroom__members__username=request.user)
        if len(user_in_group):
            group.members.remove(request.user.pk)
            return Response(data="Successfully left the group", status=status.HTTP_202_ACCEPTED)
        return Response(data="You're not a member of the group", status=status.HTTP_400_BAD_REQUEST)

        
        
