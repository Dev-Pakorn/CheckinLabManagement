from django.contrib import admin
from .models import Booking, Computer, SiteConfig, Software, UsageLog

admin.site.register(Booking)
admin.site.register(Computer)
admin.site.register(SiteConfig)
admin.site.register(Software)
admin.site.register(UsageLog)