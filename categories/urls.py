

from django.contrib import admin
from django.urls import path
from .views import list_Projects_byCategory

urlpatterns = [
    path('list_Projects_byCategory/<int:category_id>', list_Projects_byCategory,
         name="list_Projects_byCategory"),


]
