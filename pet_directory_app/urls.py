from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("pets/", views.pet_list, name="pet_list"),
    path("shelters/", views.shelter_list, name="shelter_list"),
    path("pets/<int:pk>/", views.pet_detail, name="pet_detail"),
]