from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from .models import Plant

from django.contrib.auth.models import User

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ["id", "name", "last_watered", "watering_frequency", "notes"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # We don't want to return the password in the response

    class Meta:
        model = User
        fields = ["username", "email", "password"] # Protects the other fields from unwanted updates

    def create(self, validated_data):
        # Create user and hash the password
        # Removes the password from validated data ensure the password is not set automatically in create_user()
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password) # Explicitely set password after user creation
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        # Ensure the old password is correct
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        # Use Django's built-in validation (including our custom validator)
        validate_password(value)
        return value

    def save(self, **kwargs):
        # Set the new password for the given user
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user.")

        # Explicitly check the token to make sure it's actually validated (good practice)
        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token.")

        validate_password(data["new_password"])  # Validate new password strength

        return data