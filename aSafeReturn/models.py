from django.db import models
from django.conf import settings

# Create your models here.
class LightL(models.Model): #가로등
    latitude = models.FloatField(default=37.5597476) #default value: '37.5597476'
    longitude = models.FloatField(default=126.9433341) #default value: '126.9433341'

    def __str__(self):
        return str(self.id)+', '+str(self.latitude)+', '+str(self.longitude)

class ShortestL(models.Model): #최단거리 좌표
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)+', '+str(self.latitude)+', '+str(self.longitude)