from django.urls import path
from .views import donation, donationlist, singledonation, newdonation, submitDonation
from .views import donation, projectslist, newproject, editproject, deleteproject

urlpatterns = [
    path('donation', donation, name="donation"),
    path('donationlist', donationlist, name="donationlist"),
    path('singleproject/<int:id>', singledonation, name="singleproject"),
    path('newdonation', newdonation, name="newdonation"),


    path('donate/<int:id>', submitDonation, name="submit_donation"),

    path('projectslist', projectslist, name="projectslist"),
    path('newproject', newproject, name="newproject"),
    path('editproject/<int:id>', editproject, name="editproject"),
    path('deleteproject/<int:id>', deleteproject, name="deleteproject"),

]
