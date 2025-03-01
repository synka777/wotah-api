from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer
from rest_framework.permissions import IsAuthenticated

class PlantCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] # Still useful to have this here, even though we have it in settings.py
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer # Which serializer we want to use to return the data

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user) # Only return the plants that belong to the user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlantRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user)