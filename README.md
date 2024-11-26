#Setup
Git clone the project and change directory
$ git clone https://github.com/mohifalahi/blog.git
$ cd blog

Create a virtual environment and activate it
$ virtualenv venv
For Windows: $ venv\scripts\activate
For Linux: $ source venv/bin/activate

Install the requirements
(venv)$ pip install -r requirements.txt

# Run the project
To run the tests
(venv)$ python manage.py test tests.test_views

To run the project on development server on your local computer
(venv)$ python manage.py runserver

To run the project on Docker container, you can either be on the venv virtual environment or not
Run Docker Desktop (for Windows)
Run Docker Engine (for Linux) $ sudo systemctl start docker

$ docker-compose build
$ docker-compose run django python manage.py makemigrations
$ docker-compose run django python manage.py migrate
$ docker-compose up
(by running the last docker command, the tests will be run alongside the project)

Navigate to http://127.0.0.1:8000/
You can interact with the APIs using postman collection provided with the project


