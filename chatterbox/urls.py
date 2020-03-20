from django.urls import path
from .views import ThreadView, MessageView

app_name= 'chatterbox'
urlpatterns = [
    path('<username>/sms', ThreadView.as_view()),
    path('<username>/send', MessageView.as_view())
]