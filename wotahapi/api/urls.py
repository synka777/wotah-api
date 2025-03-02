from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("plants/", views.PlantListCreateView.as_view(), name="plant_list_create"),
    path("plants/<int:pk>/", views.PlantRetrieveUpdateDestroyView.as_view(), name="plant_update"),
    path("register/", views.UserRegistrationView.as_view(), name="user_registration"),
    path("reset-password/", views.ResetPasswordView.as_view(), name = "reset_password"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
