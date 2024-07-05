from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.RegisterAccountView.as_view()),
    path('accounts/login/', views.LoginAccountView.as_view()),
    path('accounts/activate/<str:uuid64>/<str:token>/',
         views.RegisterAccountView.as_view()),
]
