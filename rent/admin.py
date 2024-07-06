from django.contrib import admin
from . import models


class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ["title", "is_admin_approved"]


admin.site.register(models.Advertisement, AdvertiseAdmin)
admin.site.register(models.Review)
admin.site.register(models.AdvertisementImages)
admin.site.register(models.AdvertisementReview)
