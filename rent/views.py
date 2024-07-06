from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
