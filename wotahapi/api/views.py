from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer, UserRegistrationViewSerializer, PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .validators import CustomPasswordValidator

# Plant views
class PlantListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] # Still useful to have this here, even though we have it in settings.py
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer # Which serializer we want to use to return the data

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user) # Only return the plants that belong to the user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user)

# User views

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # This allows unauthenticated access to this view
    queryset = User.objects.all()
    serializer_class = UserRegistrationViewSerializer

    def get(self, request, *args, **kwargs):
        # Send help text as part of the response when getting a Get request
        help_text = [validator.get_help_text() for validator in CustomPasswordValidator.__subclasses__()]
        return Response({"help_text": help_text})

    def perform_create(self, serializer):
        # Save the user instance (default behavior)
        user = serializer.save()

class ResetPasswordView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]  # User must be logged in to reset their password

    def get_object(self):
        """Return the logged-in user"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)