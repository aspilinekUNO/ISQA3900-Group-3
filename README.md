# Pet Directory
A Django web application that allows users to browse, view, and manage adoptable pets from participating shelters.

## Overview
Pet Directory is a web-based application designed to help users explore adoptable pets from various shelters.
The platform provides an organized directory of pets profiles, medical information, and administrative tools for managing listings.
The goal is to streamline the adoption process by making it easier for families to find pets and for shelters to maintain accurate information.

## Features
- Homepage with featured pets
- Pet list and pet detail pages
- Shelter list
- Image upload for pet profiles and placeholder for pets without
- Admin functions to create, edit, and delete pets
- Responsive layout for mobile and desktop
- Navigation bar and consistent base template

## Tech Stack
- Python 3.10.0
- Django 5.2.12
- SQLite3 database
- HTML, CSS, & Bootstrap
- Pillow for image handling

# Installment Instructions
Clone the repository
```
git clone https://github.com/aspilinekUNO/ISQA3900-Group-3
cd ISQA3900-Group-3
```
Create and activate a virtual environment
```
python -m venv .venv
```
&emsp;&emsp; Windows Activation
```
.venv\Scripts\activate
```
&emsp;&emsp; Mac/Linux Activation
```
source .venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
Run the development server
```
python manage.py runserver
```
and view the site at http://127.0.0.1:8000/  
<br>
If you want to view admin controls, use this command:
```
python manage.py createsuperuser
```

# Using the App
- Homepage lists featured pets
- Use the navigation bar to view all pets and shelters
- Click a pet card to view more detailed information
- Admin users can log in at /admin/ to add or edit pets

# Known Issues
- No pagination on pet list or shelter list
- Limited form validation and no button to go to 'Add Pet' page
- Featured pets are currently static rather than dynamic
- Some images rely on external URLs instead of local uploads

# Future Improvements
- Add account registration and login (for users and shelter admins)
- Allow users to “favorite” pets
- Allow users to submit adoption inquiries
- Implement pagination for large pet lists
- Add automated Django tests
- Improve mobile responsiveness for certain sections
