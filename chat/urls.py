from django.urls import path
from .views import (
    DirectMessageView
)
app_name = 'chat'

urlpatterns = [
    path('<username>/dm', DirectMessageView.as_view() )
]
