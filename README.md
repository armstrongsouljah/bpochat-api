# bpochat-api
A chat application to enable users interact with one another. 

[![Build Status](https://travis-ci.com/armstrongsouljah/bpochat-api.svg?branch=staging)](https://travis-ci.com/armstrongsouljah/bpochat-api)

#### Project requirements
- Python 3.7>
- Django 2.x >
- Git
- Postgresql 10 or later
- Pipenv

#### Setup process
- clone the repo `git clone repo_name`
- navigate into the project folder
- Activate the virtualenv `pipenv shell`
- Install the project dependencies `pipenv install`
- Create a postgresql database and add a `DATABASE_URL` key value pair in a `.env` file on your local machine. 
- Run the project `python manage.py runserver`


#### Usage
#### user signup spec:
`localhost:8000/auth/signup`
{
    
    "user": {
        "username": string,
        "email":  string,
        "password": string
    }
}

#### user login spec

`localhost:8000/auth/login`

{
    "user": {
        "email":"your-email",
        "password:"your-password"
    }
}

