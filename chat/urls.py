from django.urls import path
from .views import (
    DirectMessageView
)
app_name = 'chat'

urlpatterns = [
    path('<username>', DirectMessageView.as_view() )
]
