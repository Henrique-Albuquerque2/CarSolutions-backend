from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('meusdados/', views.meusdados, name='meus_dados'),
    path('dadosusuario/<int:id>/', views.dadosusuario , name='meus_dados'),
]