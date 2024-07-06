from django.shortcuts import render
from rest_framework.views import APIView
from .models import BookProperty
from .serializers import BookPropertySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


class BookPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = BookPropertySerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save(booked_by=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        bookings = BookProperty.objects.filter(booked_by=user)
        serializer = BookPropertySerializer(bookings, many=True)
        return Response(serializer.data)
