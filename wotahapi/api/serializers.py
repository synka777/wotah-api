from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Plant

from django.contrib.auth.models import User

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"
        # fields = ["id", "name", "last_watered", "watering_frequency", "notes"]

class UserRegistrationViewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # We don"t want to return the password in the response

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # Create user and hash the password
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_pasword(self, value):
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