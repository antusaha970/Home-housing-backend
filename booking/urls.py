from django.urls import path, include
from . import views


urlpatterns = [
    path('bookings/', views.BookPropertyView.as_view()),
    path('bookings/requested/', views.PropertyOwnerView.as_view()),
    path('bookings/requested/<int:pk>/', views.PropertyOwnerView.as_view()),
]
