from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .validators import CustomPasswordValidator

# Plant views
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

# User views

class UserRegistration(generics.CreateAPIView):
    permission_classes = [AllowAny]  # This allows unauthenticated access to this view
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        # Send help text as part of the response when getting a Get request
        help_text = [validator.get_help_text() for validator in CustomPasswordValidator.__subclasses__()]
        return Response({"help_text": help_text})

    def perform_create(self, serializer):
        # Save the user instance (default behavior)
        user = serializer.save()