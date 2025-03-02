from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("plants/", views.PlantCreate.as_view(), name="plant_list_create"),
    path("plants/<int:pk>/", views.PlantRetrieveUpdateDestroy.as_view(), name="plant_update"),
    path("register/", views.UserRegistration.as_view(), name="user_registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
