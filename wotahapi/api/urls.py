from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("plants/", views.PlantCreate.as_view(), name="plant-list-create"),
]
