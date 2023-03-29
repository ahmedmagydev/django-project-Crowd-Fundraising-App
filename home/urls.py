from django.contrib import admin
from django.urls import path
from .views import home, notfound, becomevolunteer, toggle_approve_project

urlpatterns = [
    path('', home, name="home"),
    path('volunteer', becomevolunteer, name="becomevolunteer"),
    path('notfound', notfound, name="notfound"),
    path('toggle_approve_project/<int:project_id>', toggle_approve_project,
         name="toggle_approve_project"),


]
