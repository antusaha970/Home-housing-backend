from django.db import models
from django.contrib.auth.models import User
from .utils import CATEGORY_CHOICES
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])


class Advertisement(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, default=None)
    is_admin_approved = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="family")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    division = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    about = models.TextField()
    summary = models.TextField()
    title = models.CharField(max_length=255)
    rating = models.DecimalField(default=0, max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        return self.title


class AdvertisementImages(models.Model):
    image = models.ImageField(upload_to="rent/advertisement/")
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="advertisement_image")


class AdvertisementReview(models.Model):
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="advertisement_review")
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


class UserFavoriteAdvertisement(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_favorite_advertisement")
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
