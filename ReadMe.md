How to launch the project:

1. Create a new enviroment
    use 'venv' or 'conda' (I'm using conda for managing my enviroments)

    $ pip install -r requirements.txt


2. Select the enviroment
    in VSCode press 'Ctrl+Shift+P' then type Python: Select interpreter and select the enviroment 
    Note: Check if the terminal is using the enviroment (I always need to open a second one)

3. Run the server

    $ python manage.py runserver
    
    OR start debugging in VSCode by simply pressing F5 (the launch.json file is already configured)

    http://127.0.0.1:8000/ will be the default backend 


4. Read the documentation and go through the tutorial on their site
    
    https://docs.djangoproject.com/en/5.2/intro/tutorial01/

    It's well written

5. For testing web sockets you must run the project with daphne. This only works for localhost. For deployment you must create a docker container

    $ daphne your_project.asgi:application



# TODO:

    Create a 'daphne' docker container for deployment.
