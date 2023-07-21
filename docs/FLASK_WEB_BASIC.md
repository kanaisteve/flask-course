# Flask Website - Authentication, Databases & More

```
```
The goal of this notebook is to give you what you need to make a finished product that you can tweak, and turn into anything you like. Features include:
1. User Account
2. Storing Data in Database
3. Authentication
4. More...
```

**<h3>Table of Content</h3>**
```
1. Project Demo
2. Directory Structure
3. Flask Setup & Installation
4. Creating a Flask App
5. Creating Views/Route
6. Jinja Templating Engine & HTML templates
7. SignUp & Login Page
8. HTTP Methods [GET, POST]
9. Handling POST Requests
10.Message Flashing
11.SQLAlchemy Setup
12.Database Models
13.Foreign Key Relationship
14.Database Creation
15.Creating New User Account
16.Logging In Users [Flask-Login Module]
17.Checking If User Is Logged In
18.Notes HTML
19.Adding User Notes
20.Deleting User Notes
```
```
## 1. Flask Setup & Installation

`$ mkdir flask-website`

`$ cd flask-website`

`$ pipenv shell`

`$ pipenv install flask flask-login Flask-SQLAlchemy`
```

## 2. Creating a Flask App

```
# main.py
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # debug=True listens to changes in our python code and automatically re-run the webserver.
```

```
# __init__.py
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KT3245897SASG'

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
```


## 3. Create Routes/Views
```
# auth.py
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")
```

```
# views.py
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
```

## 4. Templates

### 4.1 Layout

```
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}Home{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
</head>

<body>

    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Notebook</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                    </li>
                    <!-- <li class="nav-item">
                        <a class="nav-link" href="#">Features</a>
                    </li> -->
                    <li class="nav-item">
                        <a class="nav-link" id="signUp" href="/sign-up">Sign Up</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Account
                        </a>
                        <ul class="dropdown-menu">
                            <!-- <li><a class="dropdown-item" href="#">Profile</a></li> -->
                            <li><a class="dropdown-item" id="login" href="/login">Login</a></li>
                            <li><a class="dropdown-item" id="logout" href="/logout">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz"
        crossorigin="anonymous">
    </script>
    <script 
        type="text/javascript"
        src="{{ url_for('static', filename='index.js') }}">
    </script>
</body>

</html>
```

```
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}Home{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
</head>

<body>

    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Notebook</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                    </li>
                    <!-- <li class="nav-item">
                        <a class="nav-link" href="#">Features</a>
                    </li> -->
                    <li class="nav-item">
                        <a class="nav-link" id="signUp" href="/sign-up">Sign Up</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Account
                        </a>
                        <ul class="dropdown-menu">
                            <!-- <li><a class="dropdown-item" href="#">Profile</a></li> -->
                            <li><a class="dropdown-item" id="login" href="/login">Login</a></li>
                            <li><a class="dropdown-item" id="logout" href="/logout">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz"
        crossorigin="anonymous">
    </script>
    <script 
        type="text/javascript"
        src="{{ url_for('static', filename='index.js') }}">
    </script>
</body>

</html>
```

```
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}Home{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
</head>

<body>

    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Notebook</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                    </li>
                    <!-- <li class="nav-item">
                        <a class="nav-link" href="#">Features</a>
                    </li> -->
                    <li class="nav-item">
                        <a class="nav-link" id="signUp" href="/sign-up">Sign Up</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Account
                        </a>
                        <ul class="dropdown-menu">
                            <!-- <li><a class="dropdown-item" href="#">Profile</a></li> -->
                            <li><a class="dropdown-item" id="login" href="/login">Login</a></li>
                            <li><a class="dropdown-item" id="logout" href="/logout">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz"
        crossorigin="anonymous">
    </script>
    <script 
        type="text/javascript"
        src="{{ url_for('static', filename='index.js') }}">
    </script>
</body>

</html>
```

### 4.2 Home

```
{% extends "layout.html" %}

{% block title %}Home{% endblock %}

{% block content %}
<h1>Welcome to Notebook</h1>
{% endblock %}
```

### 4.3 Sign Up

```
{% extends "layout.html" %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<div align="center">
    <form action="/submit" method='POST' class="col-6">
        <!-- Title -->
        <h2 align="center" class="my-3">Sign Up</h2>
        
        <!-- Email Address -->
        <div class="mb-3">
            <label for="email" class="form-label float-start">Email address</label>
            <input 
                type="email" 
                name="email" 
                class="form-control shadow-none" 
                id="email"
                placeholder="Enter email">
            <!-- <div id="emailHelp" class="form-text float-start">We'll never share your email with anyone else.</div> -->
        </div>

        <!-- Username -->
        <div class="mb-3">
            <label for="username" class="form-label float-start">Username</label>
            <input 
                type="text" 
                name="username" 
                class="form-control shadow-none" 
                id="username"
                placeholder="Enter first name">
        </div>

        <!-- Password -->
        <div class="mb-3">
            <label for="password1" class="form-label float-start">Password</label>
            <input type="password" name="password1" class="form-control shadow-none" id="password1" placeholder="Enter password">
        </div>

        <!-- Confirm Password -->
        <div class="mb-3">
            <label for="password1" class="form-label float-start">Password</label>
            <input type="password" name="password1" class="form-control shadow-none" id="password1" placeholder="Confirm password">
        </div>

        <!-- Form check -->
        <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="exampleCheck1">
            <label class="form-check-label float-start shadow-none" for="exampleCheck1">Check me out</label>
        </div>

        <!-- Submit -->
        <button type="submit" class="btn btn-primary shadow-none">Submit</button>
    </form>
</div>
{% endblock %}
```

### 4.4 Login

```
{% extends "layout.html" %}

{% block title %}Login{% endblock %}

{% block content %}
<div align="center">
    <form action="/submit" method='POST' class="col-6">
        <!-- Title -->
        <h2 align="center" class="my-3">Login</h2>

        <!-- Email Address -->
        <div class="mb-3">
            <label for="email" class="form-label float-start">Email address</label>
            <input 
                type="email" 
                name="email" 
                class="form-control shadow-none" 
                id="email"
                placeholder="Enter email">
        </div>

        <!-- Password -->
        <div class="mb-3">
            <label for="password1" class="form-label float-start">Password</label>
            <input type="password" name="password1" class="form-control shadow-none" id="password1"
                placeholder="Enter password">
        </div>

        <!-- Submit -->
        <button type="submit" class="btn btn-primary shadow-none">Submit</button>
    </form>
</div>
{% endblock %}
```

## 5. HTTP Request (GET, POST, etc)

### 5.1 Handling POST Request

```
# auth.py
from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            pass
        elif len(username) < 2:
            pass
        elif password1 != password2:
            pass
        elif len(password1) < 7:
            pass
        else:
            # add user to database
            pass 

    return render_template("sign_up.html")
```

## 6. Message Flashing

### 6.1 Alert Component

Add the code below in your layout or base template.

```
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}  
            {% for category, message in messages %}  
                {% if category == 'error' %}
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                {% else %}
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                {% endif %}
            {% endfor %}  
        {% endif %}  
    {% endwith %}
```

### 6.2 Update auth.py

Update the auth.py code below create flash messages in the sign-up page.

```
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password mush be at least 7 characters.', category='error')
        else:
            # add user to database
            flash('Account created!', category='success')

    return render_template("sign_up.html")
```

## 7. Flask SQLAlchemy Setup

Update the `__init__.py` file by importing SQLAlchemy and defining your database.

```
# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# define database
db = SQLAlchemy() # database object that will be used to add or delete record
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KT3245897SASG'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # initialize our database
    

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
```

### 7.1 Database Models

```
# models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # one to many relationship: a user can create many notes.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship('Note') # tell Flask and SQLAlchemy to add user's notes everytime a note is created. This relationship will be a list and will store all different notes.
```

### 7.2 Foreign Key Relationships

A foreign key is a key on one of your database tables that reference ID in another table column. A foreign key is essentally a column in your database that always references a column of another database.

In our case, we want to store the id for each user that created it. So every time a note is created, we can figure out whic user created it by looking at the `user_id`.

### 7.3 Database Creation

## 8. Creating New User Accounts

## 9. Logging In Users

### 9.1 Flask Login Module

### 9.2 Check If User Is Logged In

## 10. Notes HTML

### 10.1 Add User Notes

### 10.2 Delete User Notes


# References: 

1. [Python Website: Flask, Authentication, Database & More - YouTube Tutorial](https://www.youtube.com/watch?v=WxGBoY5iNXY&list=PL0iII0bIwvpIUC7SwtR2l09jeEUbPr4-p&index=19)

2. [Flask SQLAlchemy Doc](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

3. [PIP Install Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)

3. [PIP Install Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)

4. [Flask JWT Extended Installation](https://flask-jwt-extended.readthedocs.io/en/stable/installation.html)