from django.shortcuts import render
from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer

class PlantCreate(generics.ListCreateAPIView):
    queryset = Plant.objects.all() # What data we want to return
    serializer_class = PlantSerializer # Which serializer we want to use to return the data