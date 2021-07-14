# Group Projects API

Backend for managing group projects at the university. Web app connects students allowing them to find team members, supervisor and assign project subject. 

## Features

- sending messages between students or supervisors
- inviting to the team
- setting up and managing your team

## Technologies

- Python
- Django (rest_framework, test)

## Getting started

Download this repo and navigate to zpi-logic folder:

    git clone <some_url>
    cd zpi-logic

Create and activate virtual environment (this may differ on Linux):

    python -m venv zpi-env
    zpi-env\Scripts\activate

Install requirements inside the environment:

    pip install django
    pip install django restframework

Run your server:

    cd zpisite
    python manage.py runserver
    
To run unit tests:

    python manage.py test
    
## API Demo

After running the server try it out in browser:

    http://localhost:8000/teachers
    http://localhost:8000/students
    http://localhost:8000/getAllTeams
    
<i>API documentation in preparation</i>
    
    
