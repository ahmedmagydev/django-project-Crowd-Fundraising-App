from django.urls import path,include
# from user.views import register
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
# from .views import userprofile
from user import views


urlpatterns = [
        path('profile/<int:id>', views.showprofile , name='profile'),
        path('viewproject/<int:id>',views.user_project, name='viewproject'),
        path('deleteprofile/<int:id>',views.delete_profile,name='deleteprofile'),
        path('editprofile/<int:id>',views.update,name='editprofile'),
        path('optional/<int:id>',views.optional,name='optional'),
        
    
]