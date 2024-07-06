from django.db import models
from rent.models import Advertisement
from django.contrib.auth.models import User

# Create your models here.


class BookProperty(models.Model):
    property_ad = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="advertisement_booking")
    booked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="booked_properties")
    booked_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
