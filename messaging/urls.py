from django.urls import path
from .views import (
    MessageView
)

app_name = 'messages'
urlpatterns = [
    path('<username>/send', MessageView.as_view(), name='send'),
]