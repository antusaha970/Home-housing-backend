from rest_framework import serializers
from .models import BookProperty
from django.contrib.auth.models import User
from rent.serializers import AdvertisementSerializer


class BookedByPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class BookPropertySerializer(serializers.ModelSerializer):
    booked_by = BookedByPropertySerializer(many=False, read_only=True)

    class Meta:
        model = BookProperty
        fields = "__all__"
        extra_kwargs = {
            "booked_by": {"required": False}
        }


class BookPropertyDetailsSerializer(serializers.ModelSerializer):
    booked_by = BookedByPropertySerializer(many=False, read_only=True)
    property_ad = AdvertisementSerializer(many=False, read_only=True)

    class Meta:
        model = BookProperty
        fields = "__all__"
        extra_kwargs = {
            "booked_by": {"required": False}
        }
