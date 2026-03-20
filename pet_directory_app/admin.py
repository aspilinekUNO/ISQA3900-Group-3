from django.contrib import admin
from .models import Pet, Species, Shelter, MedicalRecord

admin.site.register(Pet)
admin.site.register(Species)
admin.site.register(Shelter)
admin.site.register(MedicalRecord)