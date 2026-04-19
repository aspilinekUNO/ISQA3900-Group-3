from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey("Species", on_delete=models.RESTRICT, null=True)
    shelter = models.ForeignKey("Shelter", on_delete=models.RESTRICT, null=True)

    age = models.PositiveIntegerField()  # WILL NEED TO BE LABELED WITH YEARS/MONTHS one or the other
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100) # probably small, med, large
    description = models.TextField(blank=True)

    ADOPTION_STATUS_CHOICES = [
        ("Available", "Available"),
        ("Pending", "Pending"),
        ("Adopted", "Adopted"),
    ]
    adoption_status = models.CharField(
        max_length=20,
        choices=ADOPTION_STATUS_CHOICES,
        default="Available",
    )

    photo = models.ImageField(upload_to="pet_photos/", blank=True, null=True)

    def __str__(self):
        return self.name

    def age_in_years(self):
        years = self.age // 12
        months = self.age % 12

        parts = []

        if years:
            year_label = "year" if years == 1 else "years"
            parts.append(f"{years} {year_label}")

        if months:
            month_label = "month" if months == 1 else "months"
            parts.append(f"{months} {month_label}")

        # If age is 0 months (unlikely, but safe)
        if not parts:
            return "0 months"

        return ", ".join(parts)

class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True) # mammal, reptile, etc

    def __str__(self):
        return self.name

class Shelter(models.Model):
    name = models.CharField(max_length=200)
    address_ln_1 = models.CharField(max_length=200)
    email = models.EmailField()
    address_ln_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    visiting_hours = models.TextField(max_length=200, blank=True)
    verified = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    pet_id = models.ForeignKey("Pet", on_delete=models.RESTRICT, null=True)
    date = models.DateField() # date that this specific record was taken/added
    description = models.TextField()
    veterinarian = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.pet_id.name} - {self.date}"

class ShelterAdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
