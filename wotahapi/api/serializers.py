from rest_framework import serializers
from .models import Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"
        # fields = ["id", "name", "last_watered", "watering_frequency", "notes"]