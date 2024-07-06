from django.urls import path, include
from . import views


urlpatterns = [
    path('bookings/', views.BookPropertyView.as_view()),
]
