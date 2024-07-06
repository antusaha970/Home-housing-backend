from django.shortcuts import render
from rest_framework.views import APIView
from .models import BookProperty
from .serializers import BookPropertySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


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


class PropertyOwnerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        bookings = BookProperty.objects.filter(property_ad__owner=user)
        serializer = BookPropertySerializer(bookings, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        booking = get_object_or_404(BookProperty, pk=pk)
        if booking.is_accepted:
            return Response({'errors': "This property has been booked already"}, status=status.HTTP_403_FORBIDDEN)

        booking.is_accepted = True
        booking.save(update_fields=["is_accepted"])

        message = f"You booking on the home housing has been approved. Please check our website for more information."
        send_mail("Booking conformation", message,
                  "noreply@gmail.com", [booking.booked_by.email])

        return Response({'details': "Approved"})
