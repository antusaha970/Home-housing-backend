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
from rest_framework.decorators import api_view
import stripe
import environ
from django.contrib.auth.models import User
env = environ.Env()
environ.Env.read_env()

stripe.api_key = env("STRIPE_SECRET_KEY")


class BookPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """This method is responsible for creating booking"""
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


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}/"


class BookPropertyWithCard(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """This method creates a stripe session with the given advertisement  and gives a url to pay"""
        YOUR_DOMAIN = env("STRIPE_PAYMENT_REDIRECT")
        user = request.user
        data = request.data
        data['user'] = user.id

        ad_id = data['property_ad']
        item = get_object_or_404(Advertisement, id=ad_id)

        checkout_order_items = [{
            'price_data': {
                'currency': 'bdt',
                'product_data': {
                    'name': item.title,
                    'metadata': {'ad_id': item.id}
                },
                'unit_amount': int(item.price * 100)
            },
            'quantity': 1,
        }]

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=checkout_order_items,
            customer_email=user.email,
            mode='payment',
            success_url=f"{YOUR_DOMAIN}/advertisements/{ad_id}/?payment=success",
            cancel_url=f"{YOUR_DOMAIN}/advertisements/{ad_id}/?payment=canceled",
            metadata=data
        )

        return Response({'session_url': session.url})


@api_view(["POST"])
def stripe_webhook(request):
    """This is stripe webhook which will be called when a successful payment happens and create a book property object in database"""
    STRIPE_WEBHOOK_KEY = env("STRIPE_WEB_HOOK_SECRET")
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_KEY)
    except ValueError as e:
        return Response({'errors': "Invalid Payload"}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return Response({'errors': "Invalid Signature"}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        data = session['metadata']

        ad = get_object_or_404(Advertisement, pk=data['property_ad'])
        user = get_object_or_404(User, pk=data['user'])

        booking_data = BookProperty.objects.create(
            property_ad=ad, booked_by=user, message=data['message'], payment_method="card", is_paid=True)
        booking_data.save()

        return Response({'details': "Payment successful"}, status=status.HTTP_200_OK)

    return Response({'details': "Unhandled event"}, status=status.HTTP_400_BAD_REQUEST)


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
