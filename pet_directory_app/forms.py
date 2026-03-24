from django import forms
from .models import Pet
from .models import Shelter

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name",
            "species",
            "shelter",
            "age",
            "breed",
            "color",
            "size",
            "description",
            "adoption_status",
            "photo",
        ]

class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = [
            "name",
            "address_ln_1",
            "address_ln_2",
            "city",
            "state",
            "zip_code",
            "phone",
            "email",
            "website",
            "visiting_hours",
            "verified",
            "admin_notes",
        ]