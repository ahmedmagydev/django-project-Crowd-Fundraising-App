from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from django.contrib import admin

# Register your models here.

from projects.models import Project, Image
admin.site.register(Project)


class MyModel(models.Model):
    my_array_field = ArrayField(models.IntegerField(), null=True, blank=True)


class MyModelAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


# admin.py
admin.site.register(Image)
