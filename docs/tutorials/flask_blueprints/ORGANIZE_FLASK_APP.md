# Structuring a Large Flask Application with Flask Blueprints

**What you'll learn:**

```
Step 1: Installing Flask and Flask-SQLAlchemy
Step 2: Creating a Configuration File
Step 3: Creating a Flask Application Factory
Step 4: Creating Flask Blueprints
        Create the Home Blueprint and Render its Templates
        Create the Posts Blueprint and Render its Templates
        Create the Questions Blueprint and Render its Templates
Step 5: Adding Flask-SQLAlchemy Models to your Flask Application
        Create a File for Managing Flask Extensions
        Create and Integrate with the Post Model
        Create and Integrate with the Question Model
Conclusion
```

* Flask provides a way to build a small web application quickly with one Python file. However, a small application can grow into a large application with multiple database tables, hundreds of routes, and complex features.
* Writing the code for a large application in one file will quickly become messy and hard to manage.
* Flask allows you to organize your application’s code base by splitting each of the application’s major parts into specific directories and files for a better-organized application

For example, in a social media application, you might have:
* the routes for users in a file called `routes.py` inside a directory called `users`
* a database model for users inside a module called `users.py` inside a models directory.
* do the same for posts, followers, hashtags, questions, answers, ads, the marketplace, payments, and other features in your large social media application. 
* If you want to edit some business logic into the payments code, you can change the database code for payments in a file loacated at `mysocialapp/models/payment.py`, then change the business logic in a a file located at `mysocialapp/payments/routes.py`.
* Each part of the application will have its code isolated in different files and directories, effectively spitting the application into easy-to-manage components.
* This structure also helps familizrize new developers with your appication soo they know where to troubleshoot an issue or add a new feature.

Flask provides a feature called `blueprints` for making application components. In the social media example, you can use blueprints to structure your large social media application with different blueprints, such as a users' blueprint, a blueprint for posts, one for followers, and so on for each feature.

In this tutorial, you will learn how to use Flask blueprints to structure a web application with tree components: the main blueprint containing the home page and other main routes, a posts blueprint for managing blog posts, and a questions blueprint for questions and answers. By the end of the tutorial, you will have built a Flask application with the following structure:

```
.
└── flask_app
    ├── src
    │   ├── extensions.py
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── models
    │   │   ├── post.py
    │   │   └── question.py
    │   ├── posts
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── questions
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       ├── index.html
    │       ├── posts
    │       │   ├── categories.html
    │       │   └── index.html
    │       └── questions
    │           └── index.html
    ├── app.db
    └── config.py
```

* Inside your `flask_app` dictionary, you'll have an `app.db` database file and a `config.py` configuration file for your Flask application.
* The main Flask application will be in the `src` directory, which will have an `__init__.py` file to make it a package for imports to work properly, and will contain function for creating the Flask application instance.
* The `src` directory will contain the `extensions.py` file for managing the Flask extensions you'll use in your application (Flask-SQLAchemy is an example of using a Flask extension). You will also have the following directories:

*`main`: the main blueprint for main routes, such as the home page.*

*`posts`: the posts blueprint for managing blog posts

* `questions`: the questions blueprint for managing questions and answers.

* `models`: the directory that will contain Flask-SQLAlchemy models.

* `templates`: the templates dirctory that will contain files for the main blueprint and a directory for each blueprint.


## Step 1: Installing Flask and Flask-SQLAlchemy

In this step we install the necessary packages for your application.

```
$ source venv/bin/activate # activate your virtual envronment
(env)kanai@localhost: $ pip install Flask Flask-SQLAlchemy
```

## Step 2: Create Configuration File

* Separating your application settings from the rest of the application and making changing settings easier.
* The configuration file will configure the `secret_key` and the `SQLAlchemy_database_URI`, and so on.
* Open a new file called `config.py`

`(env)kanaiech@localhost: $ nano config.py`

```
# flask_app/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

* Import the `os` module to access your file system.
* Use `os` to establish the base directory with `os.path.abspath(os.path.dirname(__file__)) to correctly set up the path of the database file
* Use the class named `Config` and set configuration values using class variables:
1. `SECRET_KEY`: A long random string used by Flask as a secret key, or a key used to secure the sessions that remember information from one request to another. The user can access the information stored in the session but cannot modify it unless they have the secret key, so you must never allow anyone to access your secret key. To get its value in this `config.py` file and save it in a class variable called `SECRET_KEY`, you access the environment variable’s value via the `os.environ` object using its `get()` method.
2. `SQLALCHEMY_DATABASE_URI`: The database URI specifies the database you want to establish a connection with using SQLAlchemy. You either get it from a `DATABASE_URI` environment variable or you set a default value. The default URI value here follows the format `sqlite:///path/to/app.db`. You use the `os.path.join()` function to join the base directory you constructed and stored in the basedir variable and the `app.db` file name.  
3. `SQLALCHEMY_TRACK_MODIFICATIONS`: A configuration to enable or disable tracking modifications of objects. You set it to `False` to disable tracking and use less memory

## Step 3: Creating a Flask Application Factory

At this point of the tutorial, your `flask_app` directory structure is as follows:

```
.
├── flask_app
   └── config.py
```

* The application's core code will live inside a project directory, which will be a Python package. Common directory name used are `src`, `core`, or your project's name.
* Create `__init__.py` file to hold code for your *Flask factory function*, which is a function used to set and create the Flask application instance and where you link all your Flask blueprints together.

```
(env)kanaitech@localhost: $ mkdir src
(env)kanaitech@localhost: nano src/__init__.py
```

```
# flask_app/src/__init__.py
from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
```

* Import the `Flask` class from the `flask` package.
* Then import the `Config` configuration class from the `config.py` file you created in the `flask_app` directory.
* `create_app()` function is the *Flask application factory function*. It creates an application instance called `app` from the `Flask()` class using the familiar `app = Flask(__name__)` line.
* You configure the application by importing configuration values from a object using the `app.config.from_object()` method, passing it the value of the `config_class` parameter, which holds the `Config` class as a default value. 
* Create a test route using the `app.route()` decorator inside the factory function to demonstrate how to register routes inside application factories. 
* The `create_app()` factory function returns the application instance you constructed with the line `return app`.
* Flask will automatically detect the `create_app()` factory function in your app package and use it to create an application instance. But you’ll need to set the environment variables required to run your Flask application in development mode first.
* While in your flask_app directory with your virtual environment activated, you will tell Flask where the factory function is by passing the core application’s directory name `src` as a value to the `FLASK_APP` environment variable.
* Then you will set the `FLASK_ENV` environment variable to `development` to run the application in the developemnt mode and get access to the debugger.

```
(env)kanaitech@localhost: $ export FLASK_APP=src
(env)kanaitech@localhost: $ export FLASK_ENV=development
(env)kanaitech@localhost: $ flask run
```

With the development server running, visit the following URL using your browser:

```
http://127.0.0.1:5000/test/
```

## Step 4: Creating Flask Blueprints

* Create a blueprint for the main routes that will manage the main component of your Flask application, and then you will register the blueprint on your factory function.
* Create another blueprint each for blog posts, questions and answers.
* Add a few routes to each blueprint and render templates for each route with a `templates` directory for each blueprint.

Below is how the project structures looks like:

```
.
├── flask_app
    ├── src
    │   └── __init__.py
    └── config.py
```

### 4.1 Create Home Blueprint and Render its Templates

* Leave the development server you started in the previous step running, and open a new terminal.
* Navigate to your `flask_app` directory in the new terminal. Then create a directory called `home` for your home blueprint inside the `src` directory:

```
(env)kanaitech@localhost:$ mkdir src/home
(env)kanaitech@localhost:$ nano app/home/__init__.py
```

```
# flask_app/src/home/__init__.py
from flask import Blueprint

home = Blueprint('home', __name__)
```

* Import the `Blueprint` class from the `flask` package. Use this class to create a blueprint object `home`, passing it two arguments: a name('home' in this case) and the `__name__` variable, which holds the name of the current Python module.
* With a blueprint object, which will later have routes and functions you can plug into the Flask application you create using the `create_app()` factory function.
* Next, create a `routes.py`file inside the your `home` blueprint directory, which will hold the routes fo the home blueprint.

```
(env)kanaitech@localhost:$ nano app/home/routes.py
```

```
# create routes using the home object
from src.home import home


@home.route('/')
def index():
    return 'This is The Home Blueprint'
```

* Import the `home` blueprint object from the home blueprint, which you access through `src.home`. `src` is the project's package, `home` is the home blueprint package, and `home` is the object you declared in the home blueprint's `__init__.py` file
* Use `home` object to create a `/` route and an `index()` view function with the `home.route()` decorator, similar to the `app.route()` decorator.
* Add import line at the end of the file:

```
# flask_app/src/home/__init__.py
from flask import Blueprint

home = Blueprint('home', __name__)

from app.main import routes
```

* With this addition, registering a blueprint will also register its routes.
* Next, register the blueprint inside your Flask application factory function.

```
...
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from src.home import home
    app.register_blueprint(home)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
```

* Import the `home` blueprint object from the home blueprint.
* Then use `app.register_blueprint()` method to register this home blueprint for Flask to treat as part of the application.
* The page will load the text **This is The Home Blueprint**, which is the text you returned in the home route. Now you have a blueprint with a route in your application.
* Next edit the home route in the home blueprint to render an HTML template, which will demonstrate how to render templates when working with Flask blueprints.

```
# flask_app/src/home/routes.py
from flask import render_template # renders html template
from src.home import home

@home.route('/')
def index():
    return render_template('index.html') # update this line of code
```

* Import `render_template()` function and use it in the route to render a template file called `index.html`
* Create a templates directory and base template that all other templates will share to avoid code repetition.

```
(env)kanaitech@localhost:$ mkdir src/templates
(env)kanaitech@localhost:$ nano src/templates/base.html
```

```
# flask_app/src/templates/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %} {% endblock %} - FlaskApp</title>
    <style>
        h2 {
            width: 100%;
        }

        .title {
            margin: 5px;
            width: 100%;
        }

        .content {
            margin: 5px;
            width: 100%;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }

        .post {
            flex: 20%;
            padding: 10px;
            margin: 5px;
            background-color: #f3f3f3;
            inline-size: 100%;
        }

        .title a {
            color: #00a36f;
            text-decoration: none;
        }

        nav a {
            color: #d64161;
            font-size: 3em;
            margin-left: 50px;
            text-decoration: none;
        }

    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('main.index') }}">FlaskApp</a>
        <a href="#">Posts</a>
        <a href="#">Categories</a>
        <a href="#">Questions</a>
    </nav>
    <hr>
    <div class="content">
        {% block content %} {% endblock %}
    </div>
</body>
</html>
```

* The base template has a title block, some CSS, a navigation bar to link to different parts of your application, and a content block.
* Use the syntax `blueprintname.view_function_name` to link to a route when using the `url_for()` function with blueprints.
* The index page is handled by the `index()` view function in the home blueprint; therefor, you pass `home.index` to the `url_for()` function to build a link.
* Create the `index.html` file you rendered in the `index()` view function of the home bluepirnt:

```
(env)kanaitech@localhost:$ nano src/templates/index.html
```

```
# flask_app/src/templates/index.html
{% extends 'base.html' %}

{% block content %}
    <span class="title"><h1>{% block title %} The Home Page of FlaskApp {% endblock %}</h1></span>
    <div class="content">
        <h2>This is the main Flask blueprint</h2>
    </div>
{% endblock %}
```

* Extend the base template.
* Replace the content block, using `<h1>` heading that also serves as a title and an `<h2>` heading to inidcate the index page is part of the home Flask blueprint.
* With the development server running, visit the index page using your browser or refresh it if it's already open.

```
http://127.0.0.1:5000/
```

### 4.2 Create the Posts Blueprint and Rendering its Templates

* Create the blueprint for blog posts, register it, and render its templates.
* At this point, your `flask_app` directory structure is as follows:

```
.
├── flask_app
    ├── src
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       └── index.html
    └── config.py
```

```
(env)kanaitech@localhost:$ mkdir src/posts
(env)kanaitech@localhost:$ nano src/posts/__init__.py
```

```
# flask_app/src/posts/__init__.py
from flask import Blueprint

posts = Blueprint('posts', __name__)


from src.posts import routes
```

```
(env)kanaitech@localhost:$ nano src/posts/routes.py
```

```
# flask_app/src/posts/routes.py
from flask import render_template
from src.posts import posts

@posts.route('/')
def index():
    return render_template('posts/index.html')

@posts.route('/categories/')
def categories():
    return render_template('posts/categories.html')
```

* you have two routes: a route for the index page of the posts components of the application and a route for categories, which will be part of the posts component.
* In the `index` route, you render a template file with the path `posts/index.html` which means that Flask will look for a directory called `posts` in the `templates` directory and then look for an `index.html` file inside of the `posts` directory.
* In the `categories` route, you render a `categories.html` template, which will also be inside a posts directory inside the `templates` folder.

* In the `index` route, you render a template file with the path `posts/index.html` which means that Flask will look for a directory called `posts` in the `templates` directory and then look for an `index.html` file inside of the `posts` directory.

* create the `posts` directory in the `templates` directory
* Create the `index.html` file inside the `posts` file.

```
# flask_app/src/templates/posts/index.html
{% extends 'base.html' %}

{% block content %}
    <span class="title"><h1>{% block title %} The Posts Page {% endblock %}</h1></span>
    <div class="content">
        <h2>This is the posts Flask blueprint</h2>
    </div>
{% endblock %}
```

* Create a `categories.html` file inside the `posts` directory. This is the file rendered in the `categories()` view function of the posts blueprint:

```
(env)kanaitech@localhost:$ nano src/templates/posts/categories.html
```

```
# flask_app/src/templates/posts/categories.html
{% extends 'base.html' %}

{% block content %}
    <span class="title"><h1>{% block title %} Categories {% endblock %}</h1></span>
    <div class="content">
        <h2>This is the categories page within the posts blueprint</h2>
    </div>
{% endblock %}
```

* Extend the base template and set an `<h1>` heading as a title and a `<h2>` heading to mark the page as part of the posts blueprint.
* Edit the factory function by registering the posts blueprint.

```
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from src.home import home
    app.register_blueprint(home)

    from src.posts import posts
    app.register_blueprint(posts, url_prefix='/posts')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
```

* Import the `posts` blueprint object from the posts blueprint package.
* Register the posts blueprint using the `app.register_blueprint()` method by passing it the `posts` blueprint object.
* Pass the object as a value `'/posts'` for the `url_prefix` parameter, which will prefix the blueprint's routes with this string.
* With new posts blueprint registered and development server running, use your browser to navigate to the following URLs:

```
http://127.0.0.1:5000/posts/
http://127.0.0.1:5000/posts/categories/
```

To make the **Posts** and **Categories** links in the navigation bar functional, open the base template for modification:

```
<nav>
    <a href="{{ url_for('home.index') }}">FlaskApp</a>
    <a href="{{ url_for('posts.index') }}">Posts</a>
    <a href="{{ url_for('posts.categories') }}">Categories</a>
    <a href="#">Questions</a>
</nav>
```

* You link to the posts index with `url_for('posts.index')` function call and the categories page with `url_for('posts.categories').
* Refresh any page in your application to enable the Posts and Categories link functionality.

### 4.2 Create the Questions Blueprint and Rendering its Templates

* Create the questions blueprint, register it, and render its templates.
* At this point of the project, your `flask_app` directory structure is as follows (excluding virtual environment):

```
.
├── flask_app
    ├── src
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── posts
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       ├── index.html
    │       └── posts
    │           ├── categories.html
    │           └── index.html
    └── config.py
```

```
(env)kanaitech@localhost:$ mkdir src/questions
(env)kanaitech@localhost:$ nano src/questions/__init__.py
```

Create a `question` blueprint object and import the routes that you'll later create in the blueprint's `routes.py` file:

```
# flask_app/src/questions/__init__.py
from flask import Blueprint

questions = Blueprint('questions', __name__)

from src.questions import routes
```

* Next, open `routes.py` file inside the questions blueprint:

```
(env)kanaitech@localhost:$ nano nano src/questions/routes.py
```

```
# flask_app/src/questions/routes.py
from flask import render_template
from src.questions import questions

@questions.route('/')
def index():
    return render_template('questions/index.html')
```

* Create `/` route using the `questions` blueprint object, rendering a template file called `index.html` inside a dirctory called `questions`, which will be created inside the templates folder.
* Create `question` directory inside the templates directory, and then open an `index.html` file in it:

```
(env)kanaitech@localhost:$ mkdir src/templates/questions
(env)kanaitech@localhost:$ nano/templates/questions/index.html
```

* Update the app.py

```
# flask_app/src/__init__.py
from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

# Initialize Flask extensions here

    # Register blueprints here
    from src.home import home
    app.register_blueprint(home)

    from src.posts import posts
    app.register_blueprint(posts, url_prefix='/posts')

    from src.questions import questions
    app.register_blueprint(questions, url_prefix='/questions')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
```

* With your development server running, use your browser to navigate to the following URL:
    
```
http://127.0.0.1:5000/questions/
```

The **Questions** and **Questions Blueprint** headings will be displayed on the page.

Open the base template to edit the navigation bar:

```
(env)kanaitech@localhost:$ nano/templates/base.html
```

Modify the `<nav>` tag with the highlighted expression:

```
<nav>
    <a href="{{ url_for('main.index') }}">FlaskApp</a>
    <a href="{{ url_for('posts.index') }}">Posts</a>
    <a href="{{ url_for('posts.categories') }}">Categories</a>
    <a href="{{ url_for('questions.index') }}">Questions</a>
</nav>
```

* Link to the question index page using the `url_for('questions.index')` function call.
* Refresh any page in your application to enable the **Question** link functionality in the navigation bar.

## Step 5: Add Flask-SQLAlchemy Models to Flask App

* Add a directory for database models, and create a model for posts and one for questions.
* Insert a few blogs into the posts table, then edit the posts' index route to display all posts in the database.
* Insert a few questions and answers into the questions table to display them on the questions' index page, alongside a new web form for adding further questions and answers to the database.
* At this point of the project, your `flask_app` directory structure is as follows (excluding the virtual environment's directory):

```
.
├── flask_app
    ├── src
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── posts
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── questions
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       ├── index.html
    │       ├── posts
    │       │   ├── categories.html
    │       │   └── index.html
    │       └── questions
    │           └── index.html
    └── config.py
```

### 4.1 Creating a File for Managing Flask Extensions and Integrating Flask-SQLAlchemy

* Add a Python module called `extensions.py` in which you'll set up your various Flask extensions, to your `src` directory.
* Open new `extensions.py` file inside your `src` directory.

```
(env)kanaitech:$ nano src/extensions.py
```

```
# flask_app/src/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

* Import the `SQLAlchemy()` class from the Flask-SQLAlchemy package, then use it to create a `db` database object with no arguments.
* Use `db` object to integrate SQLAlchemy with the Flask application you construct in your factory function.

```
(env)kanaitech:$ nano src/__init__.py
```

```
# flask_app/src/__init__.py
from flask import Flask

from config import Config
from app.extensions import db # import extensions

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app) # create and interact with Flask-SQLAlchemy models

    # Register blueprints here
    from src.home import home
    app.register_blueprint(home)

    from src.posts import posts
    app.register_blueprint(posts, url_prefix='/posts')

    from src.questions import questions
    app.register_blueprint(questions, url_prefix='/questions')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
```

* import the `db` database object from the `app.extensions` module.
* Before registering blueprints, connect the database object to the `app` application instance using the `db.init_app()` method.
* With this, use `db` object to create and interact with Flask-SQLAlchemy models in your application.
* Remember that you've configured Flask-SQLAlchemy using the `Config` object in the `config.py` file inside your `flask_app` directory. Let's have a quick look:

```
# flask_app/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

* If you don't set up a `DATABASE_URI` environment variable, the `db` object will, by default, connect to an SQLite file called `app.db` that will appear in your `flask_app` directory once you create your database tables.
* Close the file when finished reviewing it.
* Check that the database was registered correctly using the Flask shell


```
(env)kanaitech@localhost:$ export FLASK_APP=app
(env)kanaitech@localhost:$ export FLASK_ENV=development
(env)kanaitech@localhost:$ flask shell

>>> from src.extensions import db
>>> print(db)

Output:
<SQLAlchemy engine=sqlite:///your_path_to_flask_app/app.db>
```

* The output means that the `db` object was properly registered. 
* If you get an error running the code in the Flask shell, ensure you've registered the `db` object correctly in your factory before moving to the next section.
* Exit the Flask shell by typing `exit()`.

## 4.2 Creating and Integrating with the Post model

* Large applications have hundreds of database tables, which means you would need to write hundreds of SQLAlchemy models to manage them.
* Putting all your models in one file will make your application hard to maintain, so you will spit your model into separate Python files inside a `models` directory.
* Each fill will hold the models and functions related to a specific part of your application.
* For example, put models and functions for managing posts inside a `post.py` file in a directory called `models` in the `app` directly.
* At this point in the project, your `flask_app` directory structure is as follows (excluding the virtual environment's directory):

```
.
├── flask_app
    ├── app
    │   ├── extensions.py
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── posts
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── questions
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       ├── index.html
    │       ├── posts
    │       │   ├── categories.html
    │       │   └── index.html
    │       └── questions
    │           └── index.html
    └── config.py
```

* First create a directory called `models` inside your `src` directory.
* Then open a new file called `post.py` inside your models directory.

```
(env)kanaitech@localhost:$ mkdir src/models
(env)kanaitech@localhost:$ nano src/models/post.py
```

```
# flask_app/src/models/post.py
from src.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.title}">'
```

* Import the `db` database object from the `app.extensions` module.
* Then create a Flask-SQLAlchemy database model called `Post` using the `db.Model` class.
* In the model, ID integer column is a primary key (`id`), a column to hold strings for the post title (`title`), and a text column for content (`content`).
* Use the special `__repr__()` method to provide a string representation for each post object using its title.

```
(env)kanaitech@localhost:$ flask shell

>>> from src.extensions import db
>>> from src.models.post import Post
>>> db.create_all()
```

The code should execute without an output. If you receive an error, check your `src/extensions.py` and `src/models/post.py` files.

```
>>> db.drop_all()
>>> db.create_all()
```

* Run this two commands if you want to apply the modifications you make to your models in the database.
* To update the database and preserve existing data, you’ll need to use the Flask-Migrate extension to perform SQLAlchemy schema migrations through the Flask command-line interface.

Next, create ten random posts:

```
>>> import random
>>>
>>> for i in range(0, 10):
>>>     random_num = random.randrange(1, 1000)
>>>     post = Post(title=f'Post #{random_num}', content=f'Content #{random_num}')
>>>     db.session.add(post)
>>>     print(post)
>>>     print(post.content)
>>>     print('--')
>>>     db.session.commit()
```

* import the `db` database object, the `Post` database model, and the `random` Python module to generate random numbers
* use `for` loop with the `range()` Python function to repeat a code block ten times.
* In the `for` loop, use `random.randrange()` method to generate a random integer number between `1` and `1000` and save it to a variable called `random_num`.
* Create a `post` object using the `Post` model and use the random number in the `random_num` variable to generate a sample post title and content.
* Then add the post object to the database session, print the object itself and its content, and commit the transaction.
* Below is a similar output you'll receive:

`Output:`

```
<Post "Post #58">
Content #58
--
<Post "Post #55">
Content #55
--
<Post "Post #994">
Content #994
--
<Post "Post #394">
Content #394
--
<Post "Post #183">
Content #183
--
<Post "Post #633">
Content #633
--
<Post "Post #790">
Content #790
--
<Post "Post #883">
Content #883
--
<Post "Post #259">
Content #259
--
<Post "Post #581">
Content #581
--
```

* Each post has a randomly generated number attaced to it.
* These posts will now be in your database.
* Edit the import and the index routes by adding the highligheted lines:


```
# flask_app/app/posts/routes.py
from flask import render_template
from src.posts import posts
from src.extensions import db
from src.models.post import Post

@posts.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)
```

* Here, you import the `db` database object and the `Post` model.
* Get all the posts in the database and then pass them to the posts' index template.
* Open the post's index template for modification to display the posts you passed to it:

```
# flask_app/src/templates/posts/index.html
{% extends 'base.html' %}

{% block content %}
    <span class="title"><h1>{% block title %} The Posts Page {% endblock %}</h1></span>
    <div class="content">
        <h2>This is the posts Flask blueprint</h2>
        {% for post in posts %}
            <div class="post">
                <p><b>#{{ post.id }}</b></p>
                <p class="title">
                    <b>
                        <a href="#">
                            {{ post.title }}
                        </a>
                    </b>
                </p>
                <div class="content">
                    <p>{{ post.content }}</p>
                </div>
                <hr>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

* Loop through posts and display each post's ID, title, and content
* With the development server running, visit the post's index page or refresh it if you have it open:

```
http://127.0.0.1:5000/posts/
```

### 4.3 Create and Integrate with Question Model

* You have created a post model and interacted with it in your posts blueprint.
* Now add the question database model for managing questions and answers.
* At this point in your project, your `flask_app` directory structure is as follows (excluding the virtual environment's directory):

```
.
├── flask_app
    ├── app
    │   ├── extensions.py
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── models
    │   │   └── post.py
    │   ├── posts
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── questions
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── base.html
    │       ├── index.html
    │       ├── posts
    │       │   ├── categories.html
    │       │   └── index.html
    │       └── questions
    │           └── index.html
    ├── app.db
    └── config.py
```

* Open a new new file called `question.py` inside your models directory:

```
(env)kanaitech@localhost:$ nano src/model/question.py
```

```
# flask_app/src/models/question.py
from src.extensions import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    answer = db.Column(db.Text)

    def __repr__(self):
        return f'<Question {self.content}>'
```

* Here, import the `db` database object from the `src.extensions` module.
* Then create a model called `Question` using the `db.Model` class.
* In the model, you have an ID integer column as a primary key (`id`), a text column for the question's content(`conten`), and a text column for its answer (`answer`).
* Then you use the `__repr__()` method to represent each question using its content.

```
(env)kanaitech@localhost:$ flask shell

>>> from src.extensions import db
>>> from src.models.question import Question
>>> db.create_all()

>>> q1 = Question(content='Why is the sky blue?', answer='Because... Why not?')
>>> q2 = Question(content='What is love?', answer='A portal to the underworld.')
>>> db.session.add_all([q1, q2])
>>> db.session.commit()
```

* The code should execute without an output. If you receive an error, check your `app/models/question.py` file to ensure your code is written with the correct syntax.
* Import the database object and the question model, then use `db.create_all()` to create the table. Finally, add two question object to the database session and commit the transaction.

```
(env)kanaitech@localhost:$ exit()
```

* You can now interact with the new question model in your questions blueprint.
* First, open the questions blueprint's `routes.py` file for a modification to query and display the questions you have in your questions table:

```
# flask_app/app/questions/routes.py
from flask import render_template
from src.questions import questions
from src.models.question import Question

@questions.route('/')
def index():
    questions = Question.query.all()
    return render_template('questions/index.html', questions=questions)
```

* Here, you import the questions model
* Get all the questions in the database, and then
* Pass them to the questions' index template.
* Next, display the questions you passed to the questions' index template and add a web form to allow users to add new questions.
* Open the `index.html` file in the questions' template directory.

```
(env)kanaitech:$ nano src/templates/questions/index.html
```

```
{% extends 'base.html' %}

{% block content %}
    <span class="title">
        <h1>{% block title %} Questions {% endblock %}</h1>
    </span>
    <div class="questions">
        <h2>Questions Blueprint</h2>

        <div class="question">
            <div class="new-question">
                <form method="POST">
                    <p>
                        <textarea id="q-content"
                                name="content"
                                placeholder="Question"
                                cols="30" rows="3"></textarea>
                    </p>
                    <textarea id="q-answer"
                            name="answer"
                            placeholder="Answer"
                            cols="30" rows="3"></textarea>
                    <p><input type="submit"></p>
                </form>
            </div>
            <div class="questions-list">
                {% for question in questions %}
                    <div class="question">
                        <h4>{{ question.content }}</h4>
                        <p>{{ question.answer }}</p>
                        <hr>
                    </div>
                {% endfor %}
            </div>
        </div>

    </div>
{% endblock %}
```

* Here, create a form with two text areas: one for the question's content and one for its answer.
* Then add a submit button for the form
* Below the form, loop through the `questions` variable you passed from the questions' index route, displaying each question's content and answer.
* With your development server running, use your browser to navigate to the questions index page:

```
http://127.0.0.1:5000/questions/
```

**Filling in the Form**

* Filling in and submitting the form will result in a `405 Method Not Allowed` HTTP error because the form sends a 'POST' reqeust to the questions' index route, but the rout does not accept nor handle `POST` requests.
* To resolve this issue and make the form functional, modify the index route of the questions blueprint and use the form data to add new questions to the database.
* Open the questions blueprint's `routes.py` file:

```
(env)kanaitech@localhost:$ nano src/questions/routes.py
```

```
# flask_app/app/questions/routes.py
from flask import render_template, request, url_for, redirect
from src.questions import questions
from src.models.question import Question
from src.extensions import db

@questions.route('/', methods=('GET', 'POST'))
def index():
    questions = Question.query.all()

    if request.method == 'POST':
        new_question = Question(content=request.form['content'],
                                answer=request.form['answer'])
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('questions.index'))

    return render_template('questions/index.html', questions=questions)
```

* Allow the `GET` and `POST` methods by passing the `('GET', 'POST')` tuple to the `methods` parameter.
* You handle `POST` requests in the `if request.method == 'POST':` condition. In it, create a new question object using the content and answer the user submits, which you get from the `request.form` object.
* Add the new question to the database session, commit the transaction, and then redirect the user to the questions index page.
* The form will now work, and you can add new questions and answers to your database.
* Test this functionality at the `http://127.0.0.1:5000:/questions/` URL

## Conclusion

You have structured a large Flask application using blueprints and organized it with templates and models. You set it up so that each component has its own routes, templates, and models.

The example web application now has three major components that can be expanded upon in different ways:
* The home blueprint: you can add an about page or a contact page for users to contact the application owner.
* The posts blueprint: you can add pages for creating, editing, deleting, and sorting posts. You can als add tags to posts using a [Many-to-Many database relationship with Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalche).
* The question blueprint: you can add pages for managing questions and use a [One-to-Many database relationship with Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-use-one-to-many-database-relationships-with-flask-sqlalchemy) to create another table for answers so that a question can have multiple solutions.

# References

1.[How To Structure a Large Flask Application with Flask Blueprints and Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy)

2. [How To Build Web Applications with Flask](https://www.digitalocean.com/community/tutorial-series/how-to-create-web-sites-with-flask)

3. [How To Build Web Applications with Flask](https://www.digitalocean.com/community/tutorial_series/how-to-create-web-sites-with-flask)