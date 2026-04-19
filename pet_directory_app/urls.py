from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path('', views.index, name="index"),
    path("pets/", views.pet_list, name="pet_list"),
    path("shelters/", views.shelter_list, name="shelter_list"),
    path("pets/<int:pk>/", views.pet_detail, name="pet_detail"),
    path("pets/<int:pk>/medical/", views.pet_medical_records, name="pet_medical_records"),
    path("pets/add/", views.pet_create, name="pet_create"),
    path("pets/<int:pk>/edit/", views.pet_update, name="pet_update"),
    path("pets/<int:pk>/delete/", views.pet_delete, name="pet_delete"),
    path("shelters/add/", views.shelter_create, name="shelter_create"),
    path("shelters/<int:pk>/edit/", views.shelter_update, name="shelter_update"),
    path("shelters/<int:pk>/delete/", views.shelter_delete, name="shelter_delete"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path("pets/<int:pk>/contact/", views.contact_shelter, name="contact_shelter"),

]