from django.contrib import admin
from . import models

admin.site.register(models.Advertisement)
admin.site.register(models.Review)
admin.site.register(models.AdvertisementImages)
admin.site.register(models.AdvertisementReview)
