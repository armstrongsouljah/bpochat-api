from django.urls import path
from .views import(
    RegistrationView,
    LoginAPIView,
    UserListView
)

app_name = 'authentication'

urlpatterns = [
    path('signup', RegistrationView.as_view(), name='signup'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='clients')
]