from django.urls import path, include
from . import views


urlpatterns = [
    path('bookings/', views.BookPropertyView.as_view()),
    path('bookings/web-hook/', views.stripe_webhook),
    path('bookings/card/', views.BookPropertyWithCard.as_view()),
    path('bookings/requested/', views.PropertyOwnerView.as_view()),
    path('bookings/requested/<int:pk>/', views.PropertyOwnerView.as_view()),
    path("bookings/successful-payment/", views.successFulPayment),
    path("bookings/cancel-payment/", views.cancelPayment)
]
