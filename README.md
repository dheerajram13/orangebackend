# Introduction

The goal of this project is to make an API to fetch all the time slots and book a available time slot with the customer details. 

# Getting Started
1. Clone this repo in your machine. [Git link](https://github.com/dheerajram13/orangebackend.git).
2. Install Python3 in your machine. [Download Python](https://www.python.org/downloads/).
3. Install postgresql and create a DB.
4. Create a `.env` file where manage.py file exists, with the following data. 
    ```
    DEBUG=
    SECRET_KEY=
    DB_NAME=
    DB_USER=
    DB_PASS=
    DB_HOST=localhost
    DB_PORT=5432

    ```
5. Create a virtual env and activate the env. 
6. Type the following commands in your terminal:
    ```
        pip install -r requirements.txt
        python manage.py makemigrations
        python manage.py migrate
    ```

7. To start the web server, type the below command:
    ```sh
    $ python manage.py runserver
    ```
8. I've created this for the production environment. Just to make automate reset the slots everday. To add the crontab (run it only once, else it will create multiple cronjob for the same thing. use show to check the existing cronjobs)
    ```sh
    $ python manage.py crontab add 
    ```

### Getting Started with the API 
1. Open http://127.0.0.1:8000/api/slots/ in your browser or postman.
2. To book a time slot open http://127.0.0.1:8000/api/book-slot/ in postman 
    * POST Request(JSON) : {"name":"John",
                "phone":"8285353102",
                "time":"11AM-12PM"
                }
    * Response: {"is_success": true,
                "slot_id": "bfb40d96-4dcf-4e48-8c68-e24c53968be5"
                }
 

## Screenshots
* All time slots API 
![Default Home View](screenshots/1.PNG?raw=true "All time slots API")

* Book a time slot API  
![Default Home View](screenshots/2.PNG?raw=true "Book a time slot API")




