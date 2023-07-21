# Introduction to Flask 

## What is Flask?

Flask is a module that leaves almost all design and architecture decisions up to the developer. It is basically a super lightweight python framework with useful tools that allows you to make website really quickly and really easily. It's not powerful as Django and is not usually used in production application. Flask teaches the fundamentals of web development. It can be used to build a small website or MVP.

## Why Use Flask?

* Flask is simple, easy to setup and easy to use.
* Flask offers a lot of flexibility leaving all designs and architecture decisions up to the developer.
* Flask offers developers control their codebase with the ability to moudlarize the codebase as it grows over time.
* It provides a wide range of extensions and libraries that can be easily integrated into projects. From authentication and database management to API development and testing.
* Shallow Learning Curve. Understanding the concept of flask is not complex, that's why developers love it, even a fresher can learn Flask within a few weeks if they have a basic understanding of python programming.
* Flask is highly scalable. Most people start with a small web app idea and then scale it as per the requirements. E.g. Pintrest moved from Django to Flask and is processing billions of requests per day.
* Flask has an in-built unit testing facility that enables you to test your app before making it live in production. In addition, the framework provides features such as a built-in development server, a fast debugger, and restful request dispatching.

# Installing Flask

## Virtual environments


source: https://flask.palletsprojects.com/en/2.3.x/installation/#virtual-environments

Use a virtual environment to manage the dependencies for your project, both in development and in production.

What problem does a virtual environment solve? 
* The more Python projects you have, the more likely it is that you need to work with different versions of Python libraries, or even Python itself.
* Newer versions of libraries for one project can break compatibility in another project

Virtual environment are independent groups of Python libraries, one for each project. Packages installed for one project will not affect other projects or the operating system's packages.

### Create an environment

Create a project folder and a .venv folder within:

**1. MacOS**

`$ mkdir myproject`

`$ cd myproject`

`$ python3 -m venv .venv`

**2. Windows**

`> mkdir myproject`

`> cd myproject`

`> py -3 -m venv .venv`

### Activate the environment

Before you work on your project, activate the corresponding environment:

**1. MacOS/Linux**

`$ . .venv/bin/activate`

**2. Windows**

`> .venv\Scripts\activate`

## Install Flask

Within the activated environment, use the following command to install Flask:

`$ pip install Flask`

Flask is now installed.

# Getting Started with Flask

## 1. A Minimal Application

A minimal Flask application looks something like this:

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

So what did that code do?
1. First we imported the Flask class.
2. Next we create an instance of this class. The first argument is the name of the application's module or package. `__name__` is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows where to look for resources such as templates and static files.
3. We then use the `route()` decorator to tell Flask what the URL should trigger our function.
4. The function returns the message we want to display in the user's browser. The default content type is HTML, so HTML in the string will be rendered by the browser.

Save it as `hello.py` or something similar. Make sure to not call your application `flask.py` because this would conflict with Flask itself.


To run the application, use the `flask` command or `python -m flask`. You need to tell the Flask where your application is with the `--app` option.

`$ flask --app hello run`

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. To learn more about deploying, see [Deploying to Production](https://flask.palletsprojects.com/en/2.3.x/deploying/). 

Now head over to http://127.0.0.1:5000/, and should see your hello world greeting.

**Note:**
If the file is name `app.py` or `wsgi.py`, you don't have to use `--app`. See [Command Line Interface](https://flask.palletsprojects.com/en/2.3.x/cli/) for more details.

`$ flask run`

`$ flask --app hello run --debug`

## 2. HTML Escaping

When return HTML, any user-provided values rendered in the output must be escaped to protect from injection attacks.

```
from markupsafe import escape

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
```

`<name>` in the route captures a value from the URL and passes it to the view function.

## 3. Routing

Use the `route()` decorator to bind a function to a URL.

```
@app.route('/home')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_there():
    return 'Hello, World'
```

### 3.1 Variable Rules

You can add variable sections to a URL with `<variable_name>`. Your function then receives the `<variable_name` as a keyword argument. You can use a converter to specify the type of the argument like `<converter:variable_name>.`


```
from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
```

Converter Types:

|Type  |Description|
|------|-----------|
|String|(default) accepts any text without a slash|
|int   |accepts positive integers|
|float |accepts positive floating point values|
|path  |like string but also accepts slashes|
|uuid  |accepts UUID strings|


### 3.2 Unique URLs 

```
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

The URL for the `projects` endpoint has a trailing slash. If you access the URL without a trailing slash (`/projects`), Flask redirects you to the URL with the trailing slash (`/projects/`).

The URL for the `about` endpoint does not have a trailing slash. Accessing the URL with a trailing slash (`/about/`) produces a 404 "Not Found" error. This helps keep URL unique for these resources, which helps search engines avoid indexing the same page twice.


### 3.3 URL Building

```
from flask import url_for

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
```

```
/
/login
/login?next=/
/user/John%20Doe
```

### 3.4 HTTP Methods

Web applications use different HTTP methods when accessing URLs. By default, a route only answers to `GET` requests. You can use the `methods` arguments for the **route()** decorator to handle different HTTP methods.

```
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```

The example above keeps all methods for the route within one function.

You can also separate views for different methods into different functions. Flask provides a shortcut for decorating such routes with **get()**, **post()**, etc. for each common HTTP method.

```
@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()
```

## 4. Static Files

Dynamic web applications also need static files. That's usually where the CSS and JavaScript files are coming from. All you have to do is create a folder called `static` in your package or next to your module and it will be available at `/static` on the application.

To generate URLs for static files, use the special `static` endpoint name:

```
url_for('static', filename='style.css')
```

The file has to be stored on the filesystem as `static/style.css`

## 5. Rendering Templates

Templates can be used to generate any type of text file. For web applications, you'll be generate HTML pages, but you can also generate markdown, plain text for emails, and anything else.

To render a template you can use the `render_template()` method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments.

```
from flask import render_template

@app.route('hello')
@app.route('hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Flask will look for templates in the templates folder. If your application is a module, this folder is next to that module, if it's a package it's actually inside your package:

**Case 1: a module**
```
/application.py
/templates
    /hello.html
```
**Case 2: a package**
```
/application
    /__init__.py
    /templates
        /hello.html
```

For templates you can use the full power of Jinja2 templates. See the offical [Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/) for more information. Below is an example template:

```
# templates/hello.html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
    <h1>Hello {{ name }}!</h1>
{% else %}
    <h1>Hello, World!</h1>
{% endif %}
```

Inside templates you also have access to the **config**, **request**, **session** and **g** objects as well as the **url_for()** and **get_flashed_messages()** functions.

Templates are useful in [Template Inheritance](https://flask.palletsprojects.com/en/2.3.x/patterns/templateinheritance/) which makes it possible to keep certain elements on each page (like header, navigation and footer).

Automatic escaping is enabled. You can mark an HTML element safe using the **Markup** class or by using the `|safe` filter in the template. Check out the Jinja 2 documentation for more examples.

```
from markupsafe import Markup
Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
```

OUTPUT:

`Markup('<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')`

```
Markup('<blink>hacker</blink>')
```

OUTPUT:

`Markup('<blink>hacker</blink>')`

```
Markup('<em>Marked up</em> &raquo; HTML').striptags()
```

`'Marked up » HTML'`

## 6. Accessing Request Data

In web applications, it's crucial to react to the data a client sends to the server.The global **request** object provides this information in Flask.

### 6.1 The Request Object

First import it from the `flask` module:

```
from flask import request
```

The current request method is available by using the **method** attribute. To access form data (data transmitted in a `POST` or`PUT` request) you can use the **form** attribute. Below is an example:

```
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
```

To access parameters submitted in the URL (`?key=value`) you can use the args attribute:

```
searchword = request.args.get('key', '')
```

### 6.2 File Upload

### 6.3 Cookies

# References

1. [Virtual Environments](https://flask.palletsprojects.com/en/2.3.x/installation/#virtual-environments)
2. [Getting Starting with Flask](https://flask.palletsprojects.com/en/2.3.x/quickstart/)
3. [Flask Tutorials](https://flask.palletsprojects.com/en/2.3.x/tutorial/)
4. [Flask Templating](https://flask.palletsprojects.com/en/2.3.x/templating/)
5. [Jinja Template Engine](https://palletsprojects.com/p/jinja/)
6. [Offical Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)