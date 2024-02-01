from django.db import models

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    opening_hours = models.TextField()
    waze_link = models.TextField()
    google_link = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name