from django import forms
from .models import Pet
from .models import Shelter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # pull user out of kwargs
        super().__init__(*args, **kwargs)

        # Superusers: can choose any shelter
        if user and user.is_superuser:
            return

        # Shelter admins: restrict to THEIR shelter only
        if user and user.groups.filter(name="Shelter Admin").exists():
            admin_shelter = user.shelteradminprofile.shelter
            self.fields["shelter"].queryset = Shelter.objects.filter(id=admin_shelter.id)

        # Regular users: should never see this form, but just in case
        else:
            self.fields["shelter"].queryset = Shelter.objects.none()

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Superusers can edit everything
        if user and user.is_superuser:
            return

        # Shelter admins: hide restricted fields
        if user and user.groups.filter(name="Shelter Admin").exists():
            # Remove fields from the form entirely
            self.fields.pop("name")
            self.fields.pop("verified")
            self.fields.pop("admin_notes")

class CustomUserCreationForm(UserCreationForm):
    become_shelter_admin = forms.BooleanField(
        required=False,
        label="I want to be a shelter admin"
    )

    existing_shelter = forms.ModelChoiceField(
        queryset=Shelter.objects.all(),
        required=False,
        label="Select an existing shelter"
    )

    new_shelter_name = forms.CharField(
        max_length=200,
        required=False,
        label="Or create a new shelter"
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        become_admin = cleaned_data.get("become_shelter_admin")
        existing = cleaned_data.get("existing_shelter")
        new_name = cleaned_data.get("new_shelter_name")

        if become_admin:
            if not existing and not new_name:
                raise forms.ValidationError(
                    "Please select an existing shelter or enter a new shelter name."
                )

        return cleaned_data