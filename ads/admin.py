from django.contrib import admin

from .models import Ad, AdStatsView, AdStatsClick

admin.site.register(Ad)
admin.site.register(AdStatsView)
admin.site.register(AdStatsClick)
