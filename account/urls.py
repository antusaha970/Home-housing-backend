from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.RegisterAccountView.as_view()),
]
