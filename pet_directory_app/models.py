from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey("Species", on_delete=models.RESTRICT, null=True)
    shelter = models.ForeignKey("Shelter", on_delete=models.RESTRICT, null=True)

    age = models.PositiveIntegerField()  # WILL NEED TO BE LABELED WITH YEARS/MONTHS one or the other
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100) # probably small, med, large
    description = models.TextField(blank=True)
    adoption_status = models.CharField(max_length=100)

    photo = models.ImageField(upload_to="pet_photos/", blank=True, null=True)

    def __str__(self):
        return self.name

class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True) # mammal, reptile, etc

    def __str__(self):
        return self.name

class Shelter(models.Model):
    name = models.CharField(max_length=200)
    address_ln_1 = models.CharField(max_length=200)
    address_ln_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    visiting_hours = models.TextField(blank=True)
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
