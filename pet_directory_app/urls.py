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
    path("contact/", views.contact, name="contact"),
    path('submit-review/', views.submit_review, name='submit_review'),
    path("pets/<int:pk>/contact/", views.contact_shelter, name="contact_shelter"),
    path("manage-users/", views.user_management, name="user_management"),
    path("manage-users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("manage-users/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("manage-users/add/", views.add_user, name="user_create"),
    path("shelters/<int:shelter_id>/", views.shelter_detail, name="shelter_detail"),
    path('pet/<int:pet_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_pets, name='favorite_pets'),
    path('notifications/', views.notifications, name='notifications'),
    path("profile/", views.user_profile, name="user_profile"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password-reset/auto/", views.auto_password_reset, name="auto_password_reset"),
]
