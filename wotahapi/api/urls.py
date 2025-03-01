from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("plants/", views.PlantCreate.as_view(), name="plant-list-create"),
    path("plants/<int:pk>/", views.PlantRetrieveUpdateDestroy.as_view(), name="plant-update"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]
