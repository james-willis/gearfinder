# [Gearfinder](https://github.com/james-willis/gearfinder)
> A Flask app for buying gear on MountainProject.com

Gearfinder is a web app built on Flask for searching Mountain Project's used gear sale forum. The app aims to make 
buyers aware sooner of new posts relevant to their interests. Buyers can search the For Sale forum at any time on the 
site, or have email alerts sent to them when a new post matching their search parameters is posted. Elements of code are
inspired by or taken from [Miguel Grinberg's microblog tutorial](https://github.com/miguelgrinberg/microblog).

## Known Bugs

* Only the first page of Mountain Project's For Sale section can be searched at this time

## Installing / Getting Started
This program is written in Python 3.6. It is recommended you run the app in a virtual environment. If you are not
familiar with how to use virtual environments, you can read up on them on 
[The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Instructions for running
the website locally are below.

#### Dependencies for running the app locally
Install dependencies with pip in your virtual environment:
```shell
$ cd path/to/gearfinder
$ source path/to/venv/bin/activate
$ pip install -r requirements.txt
```
#### Set Up Environmental Variables
In your environment you will need to define three variables that the app will read from the os. Note the double quotes in the bash syntax, they're very important.

```shell
export SECRET_KEY="super-secret-long-string" # Secret Key
export EMAIL_USERNAME="\<username\>" # Username to log into the sending email account
export EMAIL_PASSWORD="\<password\>" # The password to log into the sending email account
```

[What is a secret key?](http://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key)
#### A Note on Email functionality
If you are using your email account with a google account, you will need to
[allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en).

If you are using an email account that is not a google account, you will need to modify the mail configuration settings
in ```config.py``` Documentation for flask-mail can be found [here](https://pythonhosted.org/Flask-Mail/).

### Start up the server locally
Note: Remember to set up environmental variables in each terminal window you have open!

#### The Site
 User the flask run command:
```shell
$ cd path/to/gearfinder
$ source path/to/venv/bin/activate
$ flask run
```

Once the server is running you can access the site at [localhost:5000](localhost:5000)

#### Email Server
Note: the redis-start.sh script will install redis if not already installed

0. Run the redis-start.sh script in a new terminal shell:
```shell
$ cd path/to/gearfinder
$ source path/to/venv/bin/activate
$ flask start-redis
```
0. spin up a worker:
```shell
$ cd path/to/gearfinder
$ source path/to/venv/bin/activate
$ flask start-worker
```

## Running Tests
To Come

## Deploying the app
0. Make sure requirements.txt is up to date by running 
```
flask update-requirements
```

0. Create a merge request with the [github](https://github.com/james-willis/gearfinder) repository's master branch

0. The updated app will be deployed at [gearfinder.herokuapp.com](https://gearfinder.herokuapp.com) when the request is merged

## Features
* Improved buyer searching interface for Mountain Project's For Sale Forum
* Email alerts of new for sale postings relevant to your interests


## Licensing
The code in this project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
