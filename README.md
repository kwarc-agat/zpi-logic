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

Try it out in browser:

    http://localhost:8000/teachers
