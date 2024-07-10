from django.shortcuts import render
from rest_framework.views import APIView
from .models import BookProperty
from .serializers import BookPropertySerializer, BookPropertyDetailsSerializer, RequestedPropertySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rent.models import Advertisement


class BookPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = BookPropertySerializer(data=data, many=False)
        print(data)
        if serializer.is_valid():

            ad_id = serializer.validated_data['property_ad']
            ad = get_object_or_404(Advertisement, pk=ad_id.id)
            if ad.is_booked:
                return Response({'errors': "This property is already booked"}, status=status.HTTP_403_FORBIDDEN)

            serializer.save(booked_by=user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        bookings = BookProperty.objects.filter(booked_by=user)
        serializer = BookPropertyDetailsSerializer(bookings, many=True)
        return Response(serializer.data)


class PropertyOwnerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        bookings = BookProperty.objects.filter(property_ad__owner=user)
        serializer = RequestedPropertySerializer(bookings, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        booking = get_object_or_404(BookProperty, pk=pk)
        if booking.is_accepted:
            return Response({'errors': "This property has been booked already"}, status=status.HTTP_403_FORBIDDEN)

        booking.is_accepted = True
        booking.save(update_fields=["is_accepted"])

        ad = booking.property_ad
        ad.is_booked = True
        ad.save(update_fields=["is_booked"])

        message = f"You booking on the home housing has been approved. Please check our website for more information."
        send_mail("Booking conformation", message,
                  "noreply@gmail.com", [booking.booked_by.email])

        return Response({'details': "Approved"})
