from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('filter_Projects_by_tag/<tag>', filter_Projects_by_tag,
         name="filter_Projects_by_tag"),
]
