# Pet Directory
A Django web application that allows users to browse, view, and manage adoptable pets from participating shelters.

## Overview
Pet Directory is a web-based application designed to help users explore adoptable pets from various shelters.
The platform provides an organized directory of pets profiles, medical information, and administrative tools for managing listings.
The goal is to streamline the adoption process by making it easier for families to find pets and for shelters to maintain accurate information.

## Features
### Public
- Homepage with dynamic featured pets (random, verified)
- Pet list with filters and sorting
- Pet detail pages with medical records
- Shelter list
- Image upload for pet profiles and placeholder for pets without
- Responsive layout for mobile and desktop
- Navigation bar and consistent base template
- Unverified shelters and pets will not be visible

### User and Admin Functions
- Superusers
    - View and edit all users
    - Add new users
    - Delete users (except other superusers)
    - Assign or remove Shelter Admin role
    - Filters and sorting for user list
- Role system
    - Regular users
    - Shelter Admins assigned to one specific shelter
    - Superuser (full access)

### Email Communication
- Shelter contact form
- Email notifications for adoption inquiries
- Email routing to the correct shelter

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
- Homepage lists dynamic featured pets
- Use the navigation bar to view all pets and shelters
- Click a pet card to view more detailed information
- Superusers can manage users and add pets, shelters, and users
- Email inquiries can be sent to shelters through pet detail pages

# Known Issues
- No pagination on pet list or shelter list
- Limited form validation in some areas
- No user-facing password reset flow
- Needed improvements for form layouts
- Users can add themselves as unverified admins to verified shelters

# Future Improvements
- Add email to user creation form
- Add password reset and account recovery
- Allow users to “favorite” pets
- Route emails to real addresses rather than the terminal
- Implement pagination for large pet lists
- Add automated Django tests
- Improve mobile responsiveness for certain sections
- Add shelter admin dashboards for analytics, adoption, and pet metrics