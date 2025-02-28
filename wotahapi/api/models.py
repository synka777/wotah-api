from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)
    last_watered = models.DateField(auto_now_add=True)
    watering_frequency = models.IntegerField()
    notes = models.TextField()
    
    def __str__(self):
        return self.name