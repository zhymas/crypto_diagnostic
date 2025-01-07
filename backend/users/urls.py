from django.urls import path
from .views import UserRegisterView, GetTokens, TokenRefreshView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('token', GetTokens.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
