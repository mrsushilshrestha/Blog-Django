# Django Blog API

A full-featured blog API built with Django, Django REST Framework, and JWT authentication.

## Features

- User authentication with JWT
- Create, read, update, and delete blog posts
- Comment on posts
- Like posts
- User profiles
- API documentation with Swagger

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m virtual`
3. Activate the virtual environment:
   - Windows: `virtual\Scripts\activate`
   - Unix/MacOS: `source virtual/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## API Documentation

Access the API documentation at `/swagger/` or `/redoc/` endpoints after running the server. 

