from rest_framework import serializers
from .models import Plant

from django.contrib.auth.models import User

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"
        # fields = ["id", "name", "last_watered", "watering_frequency", "notes"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # We don"t want to return the password in the response

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # Create user and hash the password
        user = User.objects.create_user(**validated_data)
        return user