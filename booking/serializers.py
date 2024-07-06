from rest_framework import serializers
from .models import BookProperty


class BookPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookProperty
        fields = "__all__"
        extra_kwargs = {
            "booked_by": {"required": False}
        }
