from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("users/me/", views.UserViews.as_view()),
    path("users/activation/", views.ActivateUserViews.as_view()),
    path("users/resend_activation/", views.ResendActivateUserViews.as_view()),
    path("users/jwt/create/", views.CreateJWT.as_view()),
    path("users/jwt/refresh/", TokenRefreshView.as_view()),
    path("users/set_password/", views.ResetUserPassword.as_view()),
]
