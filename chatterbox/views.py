from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ThreadSerializer, MessageSerializer
from .models import Thread, Message
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# from django.db.models.query import Q
from django.db.models import Q


User = get_user_model()

class ThreadView(generics.RetrieveAPIView):
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        first_user = self.request.user
        second_user = self.kwargs.get("username")
        id1 = User.objects.get(username=first_user)
        id2 =User.objects.get(username=second_user)
        try:

           obj = Thread.objects.get(first_user=id1, second_user=id2)
        except Thread.DoesNotExist:
            obj = Thread.objects.create(first_user=id1, second_user=id2)
        return obj[0]

    def get_context_data(self):
        context = super().get_context_data()
        context['messages'] = self.get_object()[0].message_set.all()
        return context


class MessageView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        username = User.objects.get(username=self.kwargs.get("username"))
        logged_in = User.objects.get(username=self.request.user)
        thread = Thread.objects.get_or_create(first_user=username, second_user=logged_in)
        request_data = {
            "message":request.data.get("message"),
            "sender_id": logged_in.pk,
            "thread_id": thread[0].pk
        }
        Message.objects.create(message=request.data.get("message"), thread=thread[0], sender=logged_in)

        return Response(data="message saved")

    def get_queryset(self):
        print(self.kwargs.get("username"))
        username = User.objects.get(username=self.kwargs.get("username"))
        logged_in = User.objects.get(username=self.request.user)
        thread1 = Thread.objects.get_or_create(first_user=username, second_user=logged_in)
        thread2= Thread.objects.get_or_create(first_user=logged_in, second_user=username)
        qs = Message.objects.filter(Q(thread=thread1[0].pk ) | Q(thread=thread2[0].pk)).order_by('timestamp')
        # qs = Message.objects.all()
        return qs
