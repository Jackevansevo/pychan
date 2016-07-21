# Pychan

An Imageboard clone written in Django. Still very much WIP

## Install Dependencies

    virtualenv -p path/to/python/installation venv
    source venv/bin/activate
    pip install -r requirements.txt


## Setup Database

    ./manage.py makemigrations boards
    ./manage.py migrate boards


## Populate with test data and run the server

    ./manage.py populate && ./manage.py runserver


