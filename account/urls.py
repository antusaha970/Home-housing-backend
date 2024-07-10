from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/', views.ProfileView.as_view()),
    path('accounts/profile/<int:pk>/', views.ProfileView.as_view()),
    path('accounts/register/', views.RegisterAccountView.as_view()),
    path('accounts/login/', views.LoginAccountView.as_view()),
    path('accounts/activate/<str:uuid64>/<str:token>/',
         views.RegisterAccountView.as_view()),
    path('accounts/favorite_ads/', views.get_all_favorites_add),
    path('accounts/published_ads/', views.get_published_advertisements),
]
