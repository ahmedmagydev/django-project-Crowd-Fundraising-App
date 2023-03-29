from django.contrib import admin

# Register your models here.

from rate.models import *


admin.site.register(Rating)

admin.site.register(ReportProject)
