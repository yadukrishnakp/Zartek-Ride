from django.db import models
from apps.user.models import Users
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Ride(models.Model):
    class StatusChoice(models.TextChoices):
        Requested   = 'Requested'
        Accepted   = 'Accepted'
        Started   = 'Started'
        InTravel  = 'InTravel'
        Completed = 'Completed'
        Cancelled = 'Cancelled'

    rider             = models.ForeignKey(Users, related_name="riders_rider", on_delete=models.CASCADE, null=True, blank=True)
    driver            = models.ForeignKey(Users, related_name="riders_driver", on_delete=models.CASCADE, null=True, blank=True)
    pickup_latitude   = models.CharField(_('Pickup Latitude'), max_length=256, null=True, blank=True)
    pickup_longitude  = models.CharField(_('Pickup Longitude'), max_length=256, null=True, blank=True)
    dropoff_latitude  = models.CharField(_('Dropoff Latitude'), max_length=256, null=True, blank=True)
    dropoff_longitude = models.CharField(_('Dropoff Longitude'), max_length=256, null=True, blank=True)
    status            = models.CharField(_('Ride Status'), max_length=256,choices=StatusChoice.choices, null=True, blank=True)
    created_at        = models.DateTimeField(_('Created At'), auto_now_add=True, editable=False, blank=True, null=True)
    updated_at        = models.DateTimeField(_('Created At'), auto_now_add=True, editable=False, blank=True, null=True)
    current_latitude  = models.CharField(_('Current Latitude'), max_length=256, null=True, blank=True)
    current_longitude = models.CharField(_('Current Longitude'), max_length=256, null=True, blank=True)
    distance_to_rider = models.CharField(_('Current Longitude'), max_length=256, null=True, blank=True)

    class Meta      : 
        verbose_name = 'Ride'
        verbose_name_plural = "Rides"

    def __str__(self):
        return str(self.rider.name)