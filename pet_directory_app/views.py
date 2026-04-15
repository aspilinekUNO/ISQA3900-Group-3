from django.shortcuts import render, get_object_or_404
from .models import Pet, Species, Shelter
from .models import MedicalRecord
from django.shortcuts import redirect
from .forms import PetForm
from .forms import ShelterForm
from django.contrib.auth.forms import UserCreationForm
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
    shelters = Shelter.objects.all()  # fetch all shelters
    return render(request, "shelter_list.html", {"shelter_list": shelters})

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, "pet_detail.html", {"pet": pet})


def pet_medical_records(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    records = MedicalRecord.objects.filter(pet_id=pet)

    return render(request, "pet_medical_records.html", {
        "pet": pet,
        "records": records
    })

def pet_create(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pet_list")
    else:
        form = PetForm()

    return render(request, "pet_form.html", {"form": form})


def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("pet_detail", pk=pet.pk)
    else:
        form = PetForm(instance=pet)

    return render(request, "pet_form.html", {"form": form})


def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == "POST":
        pet.delete()
        return redirect("pet_list")

    return render(request, "pet_confirm_delete.html", {"pet": pet})

def shelter_create(request):
    if request.method == "POST":
        form = ShelterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shelter_list")
    else:
        form = ShelterForm()
    return render(request, "shelter_form.html", {"form": form})


def shelter_update(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)
    if request.method == "POST":
        form = ShelterForm(request.POST, instance=shelter)
        if form.is_valid():
            form.save()
            return redirect("shelter_list")
    else:
        form = ShelterForm(instance=shelter)
    return render(request, "shelter_form.html", {"form": form})


def shelter_delete(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)
    if request.method == "POST":
        shelter.delete()
        return redirect("shelter_list")
    return render(request, "shelter_confirm_delete.html", {"shelter": shelter})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})