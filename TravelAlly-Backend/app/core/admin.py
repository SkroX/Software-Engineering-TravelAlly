from django.contrib import admin
from core import models

# Register your models here.

admin.site.register(models.UserModel)
admin.site.register(models.Trip)
admin.site.register(models.TripRequest)
