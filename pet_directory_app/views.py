from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def pet_list(request):
    return render(request, "pet_list.html")

def shelter_list(request):
    return render(request, "shelter_list.html")