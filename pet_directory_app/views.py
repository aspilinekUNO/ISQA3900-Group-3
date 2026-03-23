from django.shortcuts import render, get_object_or_404
from .models import Pet, Species, Shelter

def index(request):
    return render(request, "index.html")

def pet_list(request):
    species_id = request.GET.get("species")  # read ?species= from URL
    species_list = Species.objects.all()
    age_range = request.GET.get("age")
    shelter_id = request.GET.get("shelter")
    pets = Pet.objects.all()

    if species_id:
        pets = pets.filter(species_id=species_id)
    if age_range:
        if age_range == "baby":
            pets = pets.filter(age__lt=12)
        elif age_range == "young":
            pets = pets.filter(age__gte=12, age__lt=36)
        elif age_range == "adult":
            pets = pets.filter(age__gte=36, age__lt=84)
        elif age_range == "senior":
            pets = pets.filter(age__gte=84)
    if shelter_id:
        pets = pets.filter(shelter_id=shelter_id)
    context = {
        "pets": pets,
        "species_list": species_list,
        "selected_species": species_id,
        "selected_age": age_range,
        "shelter_list": Shelter.objects.all(),
        "selected_shelter": shelter_id,
    }
    return render(request, "pet_list.html", context)

def shelter_list(request):
    return render(request, "shelter_list.html")

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, "pet_detail.html", {"pet": pet})