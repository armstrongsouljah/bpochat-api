from django.urls import path
from .views import(
    RegistrationView,
)

app_name = 'authentication'

urlpatterns = [
    path('signup', RegistrationView.as_view(), name='signup')
]