from django.contrib import admin

# Register your models here.

from comments.models import *

admin.site.register(Comments)

admin.site.register(Reply)

admin.site.register(ReportComment)
