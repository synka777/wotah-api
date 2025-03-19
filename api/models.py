from django.db import models
from django.conf import settings

class Plant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Delete all plants if user is deleted
    name = models.CharField(max_length=100)
    last_watered = models.DateField(auto_now_add=True)
    watering_frequency = models.IntegerField()  # In days
    notes = models.TextField()

    def __str__(self):
        return self.name