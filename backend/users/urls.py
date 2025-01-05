from django.urls import path
from .views import UserRegisterView, GetTokens

urlpatterns = [
    path('users/register', UserRegisterView.as_view(), name='register'),
    path('users/login', GetTokens.as_view(), name='login')
]
