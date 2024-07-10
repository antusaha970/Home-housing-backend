from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('advertise', views.AdvertisementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all-advertisements/admin/', views.all_advertisement_only_for_admin),
    path('approve-advertisement-request/<int:pk>/admin/',
         views.approved_advertisement_request)
]
