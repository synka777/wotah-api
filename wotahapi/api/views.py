from rest_framework import generics, status
from .models import Plant
from .serializers import (
    PlantSerializer,
    UserRegistrationSerializer,
    PasswordResetSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.response import Response
from .validators import CustomPasswordValidator
from rest_framework.views import APIView
from django.core.mail import send_mail

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

class LoginThrottle(AnonRateThrottle):
    rate = "5/minute" # Limit to 5 login attempts per minute

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]

class UserRegistrationView(generics.CreateAPIView):
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

class ResetPasswordView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]  # User must be logged in to reset their password
    throttle_classes = [ScopedRateThrottle] # Enable throttling
    throttle_scope = "password_reset" # Use our custom rule

    def get_object(self):
        # Return the logged-in user
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permissions_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset_request" # Each view has its own throttling scope

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "If this email exists, a reset link will be sent."}, status=status.HTTP_200_OK)

            token = default_token_generator.make_token(user)
            reset_url = f"{request.scheme}://{request.get_host()}/api/password-reset/confirm/?uid={user.pk}&token={token}"

            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_url}",
                "no-reply@example.com",
                [email],
                fail_silently=False,
            )

            return Response({"detail": "Password reset link sent!"}, status=status.HTTP_200_OK)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset_confirm"

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the token
            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            # Update password
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response