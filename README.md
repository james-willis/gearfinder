# Gearfinder
> A Flask app for buying gear on MountainProject.com

Gearfinder is a web app built on Flask for searching Mountain Project's used gear sale forum. The app aims to make 
buyers aware sooner of new posts relevant to their interests. Buyers can search the For Sale forum at any time on the 
site, or have email alerts sent to them when a new post matching their search parameters is posted. Elements of code are
inspired by or taken from [Miguel Grinberg's microblog tutorial](https://github.com/miguelgrinberg/microblog).

## Known Bugs
* When a post is replied to, it registers as new again. I'm currently looking into the best way to determine
that a post is new without missing those with replies within the first 5 minutes of posting. 

* Only the first page of Mountain Project's For Sale section can be searched at this time

* Trying to create an accoutn with an email that already exists will return an error

## Installing / Getting Started
This program is written in Python 3.5. It is recommended you run the app in a virtual environment. If you are not
familiar with how to use virtual environments, you can read up on them on 
[The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Instructions for running
the website locally are below.

#### Dependencies for running the app
Install dependencies with pip in your virtual environment:
```shell
$ source path/to/venv/bin/activate
$ pip install flask
$ pip install flask_bcrypt
$ pip install flask_email
$ pip install flask_login
$ pip install flask_sqlalchemy
$ pip install sqlalchemy_migrate
$ pip install flask-wtf
$ pip install requests
$ pip install lxml
```
#### Set Up Environmental Variables
In your environment you will need to define three variables that the app will read from the os. Note the double quotes in the bash syntax, they're very important.

```shell
export SECRET_KEY="super-secret-long-string" # The [secret key](http://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key)
export EMAIL_USERNAME="\<username\>" # Username to log into the sending email account
export EMAIL_PASSWORD="\<password\>" # The password to log into the sending email account
export PORT="5000" # or any other valid port number
```

#### A Note on Email functionality
If you are using your email account with a google account, you will need to
[allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en).

If you are using an email account that is not a google account, you will need to modify the mail configuration settings
in ```config.py``` Documentation for flask-mail can be found [here](https://pythonhosted.org/Flask-Mail/).

#### Start up the server locally
 Run the run.py script in your virtual environment:
```shell
$ source path/to/venv/bin/activate
$ cd path/to/gearfinder
$ python run.py
```

Once the server is running you can access the site at [localhost:5000](localhost:5000)

## Running Tests
To Come

## Deploying the app
To Come

## Features 
* Improved buyer searching interface for Mountain Project's For Sale Forum
* Email alerts of new for sale postings relevant to your interests

## Configuration
To Come

## Licensing
The code in this project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
