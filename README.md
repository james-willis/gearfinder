# Gearfinder
> A Flask app for buying gear on MountainProject.com

Gearfinder is a web app built on Flask for searching Mountain Project's used gear sale forum. The app aims to make 
buyers aware sooner of new posts relevant to their interests. Buyers can search the For Sale forum at any time on the 
site, or have email alerts sent to them when a new post matching their search parameters is posted. Elements of code are
inspired by or taken from [Miguel Grinberg's microblog tutorial](https://github.com/miguelgrinberg/microblog).

## Installing / Getting Started
This program is written in python 3.5. It is recommended you run the app in a virtual environment. If you are not
familiar with how to use virtual environments, you can read up on them on 
[The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Instructions for running
the website locally are below:

#### Dependencies for running the app:
```shell
$ pip install flask
$ pip install flask_bcrypt
$ pip install flask_login
$ pip install flask_sqlalchemy
$ pip install sqlalchemy_migrate
$ pip install flask-wtf
$ pip install requests
$ pip install lxml
```
Note: If lxml give you installation issues...

#### Start up the server locally: 
```shell
$ source path/to/venv/bin/activate
$ cd path/to/gearfinder
$ python run.py
```

Once the server is running you can access it at [localhost:5000](localhost:5000)

## Running Tests
To Come

## Deploying the app
To Come

## Features 
* Improved buyer searching interface for Mountain Project's For Sale Forum
* To come: Email alerts of new for sale postings relevant to your interests

## Configuration
To Come

## Licensing
The code in this project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
