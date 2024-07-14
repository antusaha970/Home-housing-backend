from django.db import models
from rent.models import Advertisement
from django.contrib.auth.models import User

# Create your models here.

PAYMENT_CHOICES = (("cash", "cash"), ("card", "card"))


class BookProperty(models.Model):
    property_ad = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="advertisement_booking")
    booked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="booked_properties")
    booked_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, default="cash")
    is_paid = models.BooleanField(default=False)
