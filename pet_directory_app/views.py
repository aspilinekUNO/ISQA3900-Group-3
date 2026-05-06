from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from .models import Pet, Species, Shelter, MedicalRecord, ShelterAdminProfile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import PetForm, ShelterForm, CustomUserCreationForm, ContactShelterForm, UserEditForm, AddUserForm, ReviewForm
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group, User
from django.db.models import Q
import random

def index(request):
    # Only verified shelters + verified pets
    pets = Pet.objects.filter(shelter__verified=True)

    # Randomize and pick 3
    pet_list = list(pets)
    random.shuffle(pet_list)
    featured_pets = pet_list[:3]

    return render(request, "index.html", {
        "featured_pets": featured_pets,
    })

def is_shelter_admin(user):
    return user.groups.filter(name="Shelter Admin").exists()

def pet_list(request):
    user = request.user
    # Base queryset depends on user role
    if user.is_superuser:
        pets = Pet.objects.all()
    elif user.is_authenticated and is_shelter_admin(user):
        pets = Pet.objects.filter(
            Q(shelter__verified=True) |
            Q(shelter=user.shelteradminprofile.shelter)
        )
    else:
        # Visitors + regular users
        pets = Pet.objects.filter(shelter__verified=True)

    species_id = request.GET.get("species")  # read ?species= from URL
    species_list = Species.objects.all()
    age_range = request.GET.get("age")
    shelter_id = request.GET.get("shelter")

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
    user = request.user
    # Superusers see everything
    if user.is_superuser:
        shelters = Shelter.objects.all()
    # Shelter admins see their own shelter + verified shelters
    elif user.is_authenticated and is_shelter_admin(user):
        shelters = Shelter.objects.filter(
            Q(verified=True) | Q(id=user.shelteradminprofile.shelter.id)
        )
    # Regular users and visitors see only verified shelters
    else:
        shelters = Shelter.objects.filter(verified=True)
    return render(request, "shelter_list.html", {"shelter_list": shelters})

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    user = request.user
    # Superusers always allowed
    if user.is_superuser:
        pass
    # Shelter admin: allowed only if it's their shelter OR shelter is verified
    elif user.is_authenticated and is_shelter_admin(user):
        if not (pet.shelter.verified or pet.shelter == user.shelteradminprofile.shelter):
            return HttpResponseForbidden("You cannot view pets from unverified shelters.")
    # Regular users and visitors: only verified shelters
    else:
        if not pet.shelter.verified:
            return HttpResponseForbidden("This pet is not available.")
    return render(request, "pet_detail.html", {"pet": pet})


def pet_medical_records(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    user = request.user
    # Superusers always allowed
    if user.is_superuser:
        pass
    # Shelter admins: allowed only if it's their shelter OR shelter is verified
    elif user.is_authenticated and is_shelter_admin(user):
        if not (pet.shelter.verified or pet.shelter == user.shelteradminprofile.shelter):
            return HttpResponseForbidden("You cannot view medical records for this pet.")
    # Regular users + visitors: only verified shelters
    else:
        if not pet.shelter.verified:
            return HttpResponseForbidden("This pet is not available.")

    records = MedicalRecord.objects.filter(pet_id=pet)
    return render(request, "pet_medical_records.html", {
        "pet": pet,
        "records": records
    })

@login_required
def pet_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    if not (request.user.is_superuser or is_shelter_admin(request.user)):
        return HttpResponseForbidden("You do not have permission to add pets.")
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            pet = form.save(commit=False)
            # Shelter admins cannot override shelter
            if is_shelter_admin(request.user):
                pet.shelter = request.user.shelteradminprofile.shelter
            form.save()

            pet.save()
            return redirect("pet_list")
    else:
        form = PetForm(user=request.user)

    return render(request, "pet_form.html", {"form": form})


def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")

    if request.user.is_superuser:
        pass
    else:
        if not is_shelter_admin(request.user):
            return HttpResponseForbidden("You do not have permission to edit pets.")

        if pet.shelter != request.user.shelteradminprofile.shelter:
            return HttpResponseForbidden("You can only edit pets from your own shelter.")

    if request.user.groups.filter(name="Shelter Admin").exists():
        if pet.shelter != request.user.shelteradminprofile.shelter:
            return HttpResponseForbidden("You cannot edit pets from another shelter.")

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet, user=request.user)
        if form.is_valid():
            updated_pet = form.save(commit=False)
            # Shelter admins cannot change the shelter field
            if is_shelter_admin(request.user):
                updated_pet.shelter = request.user.shelteradminprofile.shelter
            updated_pet.save()
            return redirect("pet_detail", pk=pet.pk)
    else:
        form = PetForm(instance=pet, user=request.user)

    return render(request, "pet_form.html", {"form": form})


def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")

    if request.user.is_superuser:
        pass
    else:
        if not is_shelter_admin(request.user):
            return HttpResponseForbidden("You do not have permission to delete pets.")

        if pet.shelter != request.user.shelteradminprofile.shelter:
            return HttpResponseForbidden("You can only delete pets from your own shelter.")

    if request.method == "POST":
        pet.delete()
        return redirect("pet_list")

    return render(request, "pet_confirm_delete.html", {"pet": pet})

def shelter_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to create shelters.")
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
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
        # Superuser: full access
    if request.user.is_superuser:
        pass
    else:
        # Regular users: blocked
        if not is_shelter_admin(request.user):
            return HttpResponseForbidden("You do not have permission to edit shelters.")

        # Shelter Admins: only their own shelter
        if request.user.shelteradminprofile.shelter != shelter:
            return HttpResponseForbidden("You can only edit your own shelter.")

    if request.user.groups.filter(name="Shelter Admin").exists():
        if shelter != request.user.shelteradminprofile.shelter:
            return HttpResponseForbidden("You cannot edit another shelter.")
    if request.method == "POST":
        form = ShelterForm(request.POST, instance=shelter, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("shelter_list")
    else:
        form = ShelterForm(instance=shelter, user=request.user)
    return render(request, "shelter_form.html", {"form": form})


def shelter_delete(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers can delete shelters.")
    if request.method == "POST":
        shelter.delete()
        return redirect("shelter_list")
    return render(request, "shelter_confirm_delete.html", {"shelter": shelter})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Did they choose to become a shelter admin?
            if form.cleaned_data["become_shelter_admin"]:
                # Add to Shelter Admin group ONLY
                shelter_admin_group = Group.objects.get(name="Shelter Admin")
                user.groups.add(shelter_admin_group)

                # Determine shelter
                existing_shelter = form.cleaned_data["existing_shelter"]
                new_shelter_name = form.cleaned_data["new_shelter_name"]

                if new_shelter_name:
                    shelter = Shelter.objects.create(name=new_shelter_name)
                else:
                    shelter = existing_shelter

                # Create profile
                ShelterAdminProfile.objects.create(
                    user=user,
                    shelter=shelter
                )

            else:
                # Regular user → add to User group ONLY
                user_group = Group.objects.get(name="User")
                user.groups.add(user_group)

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def contact(request):
    pet_name = request.GET.get('pet', '')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print("New Message:")
        print(name, email, message)

        return redirect("index")

    return render(request, "contact.html", {"pet_name": pet_name})

def contact_shelter(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    shelter = pet.shelter

    if request.method == "POST":
        form = ContactShelterForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f"Adoption Inquiry for {pet.name}",
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["email"],
                recipient_list=[shelter.email],
            )
            return redirect("pet_detail", pk=pet.pk)
    else:
        form = ContactShelterForm()

    return render(request, "contact_shelter.html", {
        "form": form,
        "pet": pet,
        "shelter": shelter
    })
        
def user_management(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")

    sort = request.GET.get("sort")
    role_filter = request.GET.get("filter")

    users = User.objects.exclude(id=request.user.id)

    # FILTERING
    if role_filter == "user":
        users = users.filter(is_superuser=False).exclude(groups__name="Shelter Admin")
    elif role_filter == "admin":
        users = users.filter(groups__name="Shelter Admin")
    elif role_filter == "superuser":
        users = users.filter(is_superuser=True)

    # Annotate role + role order
    for u in users:
        if u.is_superuser:
            u.role = "Superuser"
            u.role_order = 3
            u.shelter_name = ""  # superusers have no shelter

        elif u.groups.filter(name="Shelter Admin").exists():
            u.role = "Shelter Admin"
            u.role_order = 2

            # Get the shelter name safely
            if hasattr(u, "shelteradminprofile") and u.shelteradminprofile.shelter:
                u.shelter_name = u.shelteradminprofile.shelter.name
            else:
                u.shelter_name = "(No Shelter Assigned)"

        else:
            u.role = "User"
            u.role_order = 1
            u.shelter_name = ""  # regular users have no shelter

    # SORTING
    if sort == "username_asc":
        users = sorted(users, key=lambda u: u.username.lower())
    elif sort == "username_desc":
        users = sorted(users, key=lambda u: u.username.lower(), reverse=True)
    elif sort == "role":
        users = sorted(users, key=lambda u: u.role_order)

    return render(request, "user_management.html", {
        "users": users,
        "selected_sort": sort,
        "selected_filter": role_filter,
    })

def delete_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to do this.")

    user_to_delete = get_object_or_404(User, id=user_id)

    # Superusers cannot delete other superusers
    if user_to_delete.is_superuser:
        return HttpResponseForbidden("You cannot delete another superuser.")
    # Prevent deleting yourself (extra safety)
    if user_to_delete.id == request.user.id:
        return HttpResponseForbidden("You cannot delete your own account.")

    user_to_delete.delete()
    return redirect("user_management")

def edit_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to edit users.")

    user_to_edit = get_object_or_404(User, id=user_id)

    # Cannot edit other superusers
    if user_to_edit.is_superuser:
        return HttpResponseForbidden("You cannot edit another superuser.")

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            updated_user = form.save()

            # Update role
            is_admin = form.cleaned_data["is_shelter_admin"]
            shelter = form.cleaned_data["shelter"]

            admin_group = Group.objects.get(name="Shelter Admin")

            if is_admin:
                updated_user.groups.add(admin_group)
                profile, created = ShelterAdminProfile.objects.get_or_create(
                    user=updated_user,
                    defaults={"shelter": shelter}
                )
                # If the profile already existed, update the shelter
                if not created:
                    profile.shelter = shelter
                    profile.save()
            else:
                updated_user.groups.remove(admin_group)
                ShelterAdminProfile.objects.filter(user=updated_user).delete()

            return redirect("user_management")
    else:
        form = UserEditForm(instance=user_to_edit)

    return render(request, "user_add.html", {"form": form, "user_to_edit": user_to_edit})

def add_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to add users.")

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            is_admin = form.cleaned_data["is_shelter_admin"]
            shelter = form.cleaned_data["shelter"]

            # Create the user
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Assign Shelter Admin role if needed
            admin_group = Group.objects.get(name="Shelter Admin")

            if is_admin:
                new_user.groups.add(admin_group)

                # Create profile with shelter
                ShelterAdminProfile.objects.create(
                    user=new_user,
                    shelter=shelter
                )

            return redirect("user_management")
    else:
        form = AddUserForm()

    return render(request, "user_form.html", {"form": form})

@login_required
def toggle_favorite(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.user in pet.favorited_by.all():
        pet.favorited_by.remove(request.user)
    else:
        pet.favorited_by.add(request.user)

    return redirect('pet_detail', pk=pet.id)

@login_required
def favorite_pets(request):
    pets = Pet.objects.filter(favorited_by=request.user)
    return render(request, 'favorite_pets.html', {'pets': pets})

def contact(request):
    pet_name = request.GET.get('pet', '')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print("New Message:")
        print(name, email, message)

        return redirect("index")

    return render(request, "contact.html", {"pet_name": pet_name})

def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form})
@login_required
def notifications(request):
    notifications = request.user.notification_set.all()
    return render(request, "notifications.html", {
        "notifications": notifications
    })
