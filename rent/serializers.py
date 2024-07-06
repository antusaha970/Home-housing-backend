from rest_framework import serializers
from .models import *


class AdvertiseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImages
        fields = "__all__"


class AdvertisementImageToDisplay(serializers.Serializer):
    image = serializers.ImageField()


class AdvertisementSerializer(serializers.ModelSerializer):
    is_admin_approved = serializers.BooleanField(read_only=True)
    is_booked = serializers.BooleanField(read_only=True)
    rating = serializers.DecimalField(
        read_only=True, max_digits=4, decimal_places=2)
    advertisement_image = AdvertisementImageToDisplay(
        read_only=True, many=True)

    class Meta:
        model = Advertisement
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class AdvertisementReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = AdvertisementReview
        fields = ['id', 'review']
