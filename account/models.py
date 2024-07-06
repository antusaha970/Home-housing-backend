from django.db import models
from .utills import GENDER, ROLE
from django.contrib.auth.models import User


class Profile(models.Model):
    profile_picture = models.ImageField(
        upload_to="account/profile_picture", default="account/profile_picture/profile.jpg")
    phone_number = models.IntegerField(default=None, null=True)
    gender = models.CharField(
        choices=GENDER, max_length=10, default=None, null=True)
    district = models.CharField(max_length=150, default="Dhaka")
    user_role = models.CharField(choices=ROLE, default="user", max_length=10)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="accountProfile")

    def __str__(self) -> str:
        return self.user.first_name
