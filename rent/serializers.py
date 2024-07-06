from rest_framework import serializers
from .models import *


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
