from django.db import models

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(default = "", blank=True)
    opening_hours = models.TextField(default = "", blank=True)
    waze_link = models.TextField(default = "", blank=True)
    google_link = models.TextField(default = "", blank=True)
    latitude = models.FloatField(default = "", blank=True)
    longitude = models.FloatField(default = "", blank=True)

    def __str__(self):
        return self.name