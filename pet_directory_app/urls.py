from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("pets/", views.pet_list, name="pet_list"),
    path("shelters/", views.shelter_list, name="shelter_list"),
]