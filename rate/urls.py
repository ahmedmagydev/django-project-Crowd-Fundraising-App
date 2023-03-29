
from django.urls import path
from .views import *


urlpatterns = [
    path('reportProject/<int:project_id>', reportProject, name="reportProject"),
    path('rateProject/<int:project_id>', rateproject, name="rateProject"),
    path('like_project/<int:project_id>', toggle_like, name="like_project"),
    path('toggle_like_project/<int:project_id>', toggle_like_project, name="toggle_like_project"),
]
