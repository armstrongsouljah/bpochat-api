from django.urls import path
from .views import (
    DirectMessageView,
    ChatroomView,
    GroupJoinView,
    GroupLeaveView,
    MessageThreadView
)
app_name = 'chat'

urlpatterns = [
    path('<username>', DirectMessageView.as_view()),
    path('grp/new', ChatroomView.as_view()),
    path('group/<name>/join', GroupJoinView.as_view()),
    path('group/<name>/leave', GroupLeaveView.as_view()),
    path('<username>/thread', MessageThreadView.as_view())
]
