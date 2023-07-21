# Flask Blueprints Applied

**What you'll learn:***

```
1. What is a blueprint?
   Making a Flask Blueprint
   Registering the Blueprint in your Application
2. Why Blueprints?
3. Ways to organize your App
   Functional Structure
   Divisional Structure
4. Refactoring small apps to use blueprints
   Company Website
   E-Commerce Website
```

## 1. What is a blueprint?

* A blueprint defines a collection of views, templates, static files and other elements that can be applied to an application. 

* When you register a Flask Blueprint in an application, you’re actually extending the application with the contents of the Blueprint.

* Flask Blueprint record operations to be executed later when you register them on an application.

For example, let's image that we have a blueprint for an admin panel. This blueprint would define the views for routes like */admin/login* and */admin/dashboard*. It may also include the templates and static files that will be served on those routes. We can then use this blueprint to add an admin panel to our app, be it a social network for astronauts or a CRM for rocket salesmen.

A social media application is another example, you might have:
* the routes for users in a file called `routes.py` inside a directory called `users`
* a database model for users inside a module called `users.py` inside a models directory.
* do the same for posts, followers, hashtags, questions, answers, ads, the marketplace, payments, and other features in your large social media application. 
* If you want to edit some business logic into the payments code, you can change the database code for payments in a file loacated at `mysocialapp/models/payment.py`, then change the business logic in a a file located at `mysocialapp/payments/routes.py`.
* Each part of the application will have its code isolated in different files and directories, effectively spitting the application into easy-to-manage components.
* This structure also helps familizrize new developers with your appication soo they know where to troubleshoot an issue or add a new feature.

### 1.1 Making a Flask Blueprint

```
from flask import Blueprint

example_blueprint = Blueprint('example_blueprint', __name__)
```

* some arguments are specified when creating the Blueprint object.
* The first argument, `"example_blueprint"`, is the Blueprint’s **name**, which is used by Flask’s routing mechanism.
* The second argument, `__name__`, is the Blueprint’s **import name**, which Flask uses to locate the Blueprint’s resources.

There are other optional arguments that you can provide to alter the Blueprint’s behavior:
* `static_folder`: the folder where the Blueprint’s static files can be found

* `static_url_path`: the URL to serve static files from

* `template_folder`: the folder containing the Blueprint’s templates

* `url_prefix`: the path to prepend to all of the Blueprint’s URLs

* `subdomain`: the subdomain that this Blueprint’s routes will match on by default

* `url_defaults`: a dictionary of default values that this Blueprint’s views will receive

* `root_path`: the Blueprint’s root directory path, whose default value is obtained from the Blueprint’s import name

Note that all paths, except `root_path`, are relative to the Blueprint’s directory.

Blueprint objects also provide other methods that you may find useful:
* `.errorhandler()` to register an error handler function

* `.before_request()` to execute an action before every request

* `.after_request()` to execute an action after every request

* `.app_template_filter()` to register a template filter at the application level

### 1.2. Registering the Blueprint in Your Application

When you register the Flask Blueprint in an application, you extend the application with its contents. Below is how you can register the blueprint:

```
from flask import Flask
from example_blueprint import example_blueprint

app = Flask(__name__)
app.register_blueprint(example_blueprint)
```

When you call `.register_blueprint()`, you apply all operations recorded in the Flask Blueprint example_blueprint to app. Now, requests to the app for the URL / will be served using `.index()` from the Flask Blueprint.

You can customize how the Flask Blueprint extends the application by providing some parameters to `register_blueprint`:

* `url_prefix` is an optional prefix for all the Blueprint’s routes.

* `subdomain` is a subdomain that Blueprint routes will match.

* `url_defaults` is a dictionary with default values for view arguments.

Being able to do some customization at registration time, instead of at creation time, is particularly useful when you’re sharing the same Flask Blueprint in different projects.

## 2. Why Blueprints?

The killer use-case for blueprints is to organize our application into distinct components. For a Twitter-like microblog, we might have a blueprint for the website pages, e.g. index.html and about.html. Then we could have another for the logged-in dashboard where we show all of the latest posts and yet another for our administrator’s panel. Each distinct area of the site can be separated into distinct areas of the code as well. This lets us structure our app as several smaller “apps” that each do one thing.

## 3. Ways to Organize Your App

### 3.1 Functional Structure

* With a functional structure, you organize the pieces of your app by what they do. 
* Templates are grouped together in one directory, static files in another and views in a third.

```
yourapp/
    __init__.py
    static/
    templates/
        home/
        control_panel/
        admin/
    views/
        __init__.py
        home.py
        control_panel.py
        admin.py
    models.py
```

* Each *.py* files in the *yourapp/views/* directory except *yourapp/views/__init__.py* is a blueprint.
* In the *yourapp/__init__.py* file, import these blueprints and register them on our `Flask()` object.
* If your app has largely independent pieces that only share things like models and configuration, divisional might be the way to go. 

* If the components of your app flow together a little more, it might be better represented with a functional structure.

**Example of a Division Structure:**

An example of this would be Facebook. If Facebook used Flask, it might have blueprints for: 
* the static pages (i.e. signed-out home, register, about, etc.), 
* the dashboard (i.e. the news feed),
* profiles (/robert/about and /robert/photos), 
* settings (/settings/security and /settings/privacy) 
* and many more. 

These components all share a general layout and styles, but each has its own layout as well.

```
facebook/
    __init__.py
    templates/
        layout.html
        home/
            layout.html
            index.html
            about.html
            signup.html
            login.html
        dashboard/
            layout.html
            news_feed.html
            welcome.html
            find_friends.html
        profile/
            layout.html
            timeline.html
            about.html
            photos.html
            friends.html
            edit.html
        settings/
            layout.html
            privacy.html
            security.html
            general.html
    views/
        __init__.py
        home.py
        dashboard.py
        profile.py
        settings.py
    static/
        style.css
        logo.png
    models.py
```

* The blueprints in facebook/views/ are little more than collections of views rather than wholly independent components. 
* The same static files will be used for the views in most of the blueprints.
* Most of the templates will extend a master template.

**Basice Usage**

# facebook/views/profile.py

from flask import Blueprint, render_template

profile = Blueprint('profile', __name__)

@profile.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('profile/timeline.html')

@profile.route('/<user_url_slug>/photos')
def photos(user_url_slug):
    # Do some stuff
    return render_template('profile/photos.html')

@profile.route('/<user_url_slug>/about')
def about(user_url_slug):
    # Do some stuff
    return render_template('profile/about.html')


* To create a blueprint object, we import the `Blueprint()` class and initialize it with the arguments `name` and `import_name`. 
* Usually `import_name` will just be `__name__`, which is a special Python variable containing the name of the current module.
* It’s time to register it on our Flask app.

# facebook/__init__.py

from flask import Flask
from .views.profile import profile

app = Flask(__name__)
app.register_blueprint(profile)

**Using a dynamic URL prefix**

* Blueprints let us define both static and dynamic prefixes. 
* We can tell Flask that all of the routes in a blueprint should be prefixed with `/profile` for example; that would be a static prefix. 
* In the case of the Facebook example, the prefix is going to change based on which profile the user is viewing.
* We can define the prefix in one of two places: when we instantiate the `Blueprint()` class or when we register it with `app.register_blueprint()`.

```
# facebook/views/profile.py

from flask import Blueprint, render_template

profile = Blueprint('profile', __name__, url_prefix='/<user_url_slug>')

# [...]
```

```
# facebook/__init__.py

from flask import Flask
from .views.profile import profile

app = Flask(__name__)
app.register_blueprint(profile, url_prefix='/<user_url_slug>')
```

* It’s nice to have the prefixes available in the same file as the registrations. This makes it easier to move things around from the top-level.
* For this reason, it is recommended to use `url_prefix` on registration.
* In this case we’ll want to grab the user object based on the URL slug passed into our profile blueprint. We’ll do that by decorating a function with `url_value_preprocessor()`.

# facebook/views/profile.py

from flask import Blueprint, render_template, g

from ..models import User

# The prefix is defined on registration in facebook/__init__.py.
profile = Blueprint('profile', __name__)

@profile.url_value_preprocessor
def get_profile_owner(endpoint, values):
    query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.profile_owner = query.first_or_404()

@profile.route('/')
def timeline():
    return render_template('profile/timeline.html')

@profile.route('/photos')
def photos():
    return render_template('profile/photos.html')

@profile.route('/about')
def about():
    return render_template('profile/about.html')


* We’re using the `g` object to store the profile owner and `g` is available in the Jinja2 template context. 

```
{# facebook/templates/profile/photos.html #}

{% extends "profile/layout.html" %}

{% for photo in g.profile_owner.photos.all() %}
    <img src="{{ photo.source_url }}" alt="{{ photo.alt_text }}" />
{% endfor %}
```

### 3.2 Divisional Structure

* With the divisional structure, you organize the pieces of the application based on which part of the app they contribute to.
* All of the templates, views and static files for the admin panel go in one directory, and those for the user control panel go in another.

```
yourapp/
    __init__.py
    admin/
        __init__.py
        views.py
        static/
        templates/
    home/
        __init__.py
        views.py
        static/
        templates/
    control_panel/
        __init__.py
        views.py
        static/
        templates/
    models.py
```

* Each directory under *yourapp/* is a separate blueprint.
* All of the blueprints are applied to the `Flask()` app in the top-level __init__.py

* If you’re considering spinning off your blueprints as extensions or using them for other projects, a divisional structure will be easier to work with.

**Example of a Division Structure:**

An example might be a SaaS app that lets user’s build websites. You could have blueprints in “divisions” for the 
* home page 
* the control panel 
* the user’s website
* and the admin panel. 

These components may very well have completely different static files and layouts. 

**Using a dynamic subdomain**

* Many SaaS (Software as a Service) applications these days provide users with a subdomain from which to access their software.
* Harvest, for example, is a time tracking application for consultants that gives you access to your dashboard from yourname.harvestapp.com.
* We are going to use the example of an application that lets users create their own websites.

Imagine that our app has three blueprints for distinct sections: 
* the home page where users sign-up, 
* the user administration panel where the user builds their website 
* and the user’s website.

Since these three parts are relatively unconnected, we’ll organize them in a divisional structure.

```
sitemaker/
    __init__.py
    home/
        __init__.py
        views.py
        templates/
            home/
        static/
            home/
    dash/
        __init__.py
        views.py
        templates/
            dash/
        static/
            dash/
    site/
        __init__.py
        views.py
        templates/
            site/
        static/
            site/
    models.py
```

The table explains the different blueprints in this app.

|URL          |Route                |Description|
|-------      |-------              |----------|
|sitemaker.com|sitemaker.com/home   |Just a vanilla blueprint. Views, templates and static files for index.html, about.html and pricing|
|kanai.sitemaker.com|sitemaker.com/site   |This blueprint uses a dynamic submain and includes the elements of the user's website.|
|kanai.sitemaker.com/admin|sitemaker.com/dash   |This bluepirnt could use both a dynamic subdomain and a URL prefix.|

```
# sitemaker/__init__.py

# We can define our dynamic subdomain the same way we defined our URL prefix. 
from flask import Flask
from .site import site

app = Flask(__name__)
app.register_blueprint(site, subdomain='<site_subdomain>')
```

```
# sitemaker/site/__init__py

from flask import Blueprint

from ..models import Site

# Note that the capitalized Site and the lowercase site
# are two completely separate variables. Site is a model
# and site is a blueprint.

site = Blueprint('site', __name__)

@site.url_value_preprocessor
def get_site(endpoint, values):
    query = Site.query.filter_by(subdomain=values.pop('site_subdomain'))
    g.site = query.first_or_404()

# Import the views after site has been defined. The views
# module will need to import 'site' so we need to make
# sure that we import views after site has been defined.
from . import views
```

To get Flask to work with subdomains, we’ll need to specify the SERVER_NAME configuration variable.

```
# config.py

SERVER_NAME = 'sitemaker.com'
```

## 4. Refactoring small apps to use blueprints

### 4.1 Company Website

Let's take the steps to convert an app to use blueprints. We’ll start off with a typical Flask app and restructure it.

```
config.txt
requirements.txt
run.py
src/
  __init__.py
  views.py
  models.py
  templates/
  static/
tests/
```

* The *views.py* file has grown to 10,000 lines of code.
* The sections are the home page, the user dashboard, the admin dashboard, the API and the company blog.

#### Step 1: Divisional or Function?

* This application is made up of very distinct section.
* Templates and static files probably aren't going to be shared between the user dashboard and the company blog for example.
* We'll go with a divisional structure.

#### Step 2: Move some files around

**Note:** Before you make any changes to your app, commit everything to version control. You don't want to accidentally delete something for good.

* Create the directory tree for our new app
* Start by creating a folder for each blueprint within the package directory.
* Then copy *views.py, static/* and *templates/* to each directory and remove them from the top-level package directory.

```
config.txt
requirements.txt
run.py
src/
  __init__.py
  home/
    views.py
    static/
    templates/
  dash/
    views.py
    static/
    templates/
  admin/
    views.py
    static/
    templates/
  api/
    views.py
    static/
    templates/
  blog/
    views.py
    static/
    templates/
  models.py
tests/
```

#### Step 3: Cut the Crap

* Go into each blueprint and remove the views (routes), static files and templates that don't apply to that blueprint.
* The end result should be that each blueprint has a *views.py* with all of the views for that blueprint.
* No two blueprints should define a view for the same route.
* Each *templates/* directory should only include the templates for the views(routes) in that blueprint.
* Each *static/* directory should only include the static files that should be exposed by that blueprint.

**Note:** Make sure to eliminate all unnecessary imports. It's easy to forget about them, but at best they clutter your code and at worst they slow down your application.

#### Step 4: Turn directories into blueprints

* The key is in the `__init__.py` files. 
* Let's look at the definition of the API blueprint.

```
# src/api/__init__.py

from flask import Blueprint

api = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views
```

Next we can register this blueprint in the src package’s top-level `__init__.py` file.

```
# src/__init__.py

from flask import Flask
from .api import api

app = Flask(__name__)

# Puts the API blueprint on api.src.com.
app.register_blueprint(api, subdomain='api')
```

Make sure that the routes are registered on the blueprint now rather than the app object.

```
# src/views.py

from . import app

@app.route('/search', subdomain='api')
def api_search():
    pass
```

```
# src/api/views.py

from . import api

@api.route('/search')
def search():
    pass
```

#### Step 5: Enjoy

* Now our application is far more modular than it was with one massive *views.py* file.
* The route definitions are simpler because we can group them together into blueprints and configure things like subdomains and URL prefixes once for each blueprint.

### 4.2 E-Commerce Website

In this section, we going to refactor an e-commerce site with the following features:

* Visitors can sign up, log in, and recover **passwords**
* Visitors can search for **products** and view their details.
* Users can add products to their **cart** and checkout.
* An API enables external systems to search and retrieve **product** information.

Don't focus on the details of the implementation, focus mainly on how a Flask Blueprint can be used to improve the application's architecture.

**Project Structure**

Remember, Flask does not enforce any particular project layout.

```
ecommerce/
|
├── static/
|   ├── logo.png
|   ├── main.css
|   ├── generic.js
|   └── product_view.js
|
├── templates/
|   ├── login.html
|   ├── forgot_password.html
|   ├── signup.html
|   ├── checkout.html
|   ├── cart_view.html
|   ├── index.html
|   ├── products_list.html
|   └── product_view.html
|
├── app.py
├── config.py
└── models.py
```

This application's code is organized using these directories and files:

* `static/` contains the application’s static files.

* `templates/` contains the application’s templates.

* `models.py` contains the definition of the application’s models.

* `app.py` contains the application logic.

* `config.py` contains the application configuration parameters.

This is an example of how many applications begin. Although this layout is pretty straightforward, it has several drawbacks that arise as the app complexity increases.

For example, it will be hard for you to reuse the application logic in other projects because all the functionality is bundled in `app.py`. If you split this functionality into modules instead, then you could **reuse complete modules across different projects.**

Also, if you have just one file for the application logic, then you would end up with a very large app.py that mixes code that’s nearly unrelated. This can make it hard for you to navigate and maintain the script.


**Organizing Your Projects**

You can leverage a Flask Blueprint to split the code into different modules. In this layout, there are five Flask Blueprints:
1. **API Blueprint** to enable external systems to search and retrieve product information
2. **Authentication Blueprint** to enable users to log in and recover their password
3. **Cart Blueprint** for cart and checkout functionality
4. **Home Blueprint** for the homepage
5. **Products Blueprint** for searching and viewing products

Below is how the project will look like:

```
ecommerce/
|
├── api/
|   ├── __init__.py
|   └── api.py
|
├── auth/
|   ├── templates/
|   |   └── auth/
|   |       ├── login.html
|   |       ├── forgot_password.html
|   |       └── signup.html
|   |
|   ├── __init__.py
|   └── auth.py
|
├── cart/
|   ├── templates/
|   |   └── cart/
|   |       ├── checkout.html
|   |       └── view.html
|   |
|   ├── __init__.py
|   └── cart.py
|
├── home/
|   ├── templates/
|   |   └── general/
|   |       └── index.html
|   |
|   ├── __init__.py
|   └── general.py
|
├── products/
|   ├── static/
|   |   └── view.js
|   |
|   ├── templates/
|   |   └── products/
|   |       ├── list.html
|   |       └── view.html
|   |
|   ├── __init__.py
|   └── products.py
|
├── static/
|   ├── logo.png
|   ├── main.css
|   └── generic.js
|
├── app.py
├── config.py
└── models.py

```

* This structure makes it easier for you to find the code and resources related to a given functionality.
* For example, if you want to find the application logic about products, then you can go to the Products Blueprint in `products/products.py` instead of scrolling through `app.py`.

Below is the Products Blueprint implementation in products/products.py:

```
# ecommerce/products/products.py
from flask import Blueprint, render_template
from ecommerce.models import Product

products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')

@products_bp.route('/')
def list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@products_bp.route('/view/<int:product_id>')
def view(product_id):
    product = Product.query.get(product_id)
    return render_template('products/view.html', product=product)
```

* This code defines the `products_bp` Flask Blueprint and contains only the code that's related to product functionality.
* Since this Flask Blueprint has its own templates, you need to specify the `template_folder` relative to the Blueprint's root in the Blueprint object creation.
* Since you specify `static_folder='static'` and `static_url_path='assets'`, files in `ecommerce/products/static/` will be served under the `/assets/` URL.
* Now move the rest of your code's functionality to the corresponding Flask Blueprint.
* Once you've done so, the only code left in `app.py` will be code that deals with application initilization and Flask Blueprint registration:

```
# ecommerce/app.py
from flask import Flask

from ecommmerce.api.api import api_bp
from ecommmerce.auth.auth import auth_bp
from ecommmerce.cart.cart import cart_bp
from ecommmerce.general.general import general_bp
from ecommmerce.products.products import products_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(general_bp)
app.register_blueprint(products_bp, url_prefix='/products')
```

* `app.py` simply import and registers the Blueprints to extend the application.
* `url_prefix` avoids URL collisions between Flask Blueprint routes. For example, the URLs `/products/` and `/cart/` resolve to different endpoints defined in the `products_bp` and `cart_bp` Blueprints for the same route, /

**Including Templates**

* In Flask, when a view renders a template, the template file is searched in all the directories that were registered in the application’s template search path.
* By default, this path is `["/templates"]`, so templates are only searched for in the `/templates` directory inside the application’s root directory.
* If you set the template_folder argument in a Blueprint’s creation, then its templates folder is added to the application’s template search path when the Flask Blueprint is registered.
* However, if there are duplicated file paths under different directories that are part of the template search path, then one will take precedence, depending on their registration order.

```
ecommerce/
|
└── products/
    └── templates/
        └── products/
            ├── search.html
            └── view.html
```

At first, it may look redundant to have the Flask Blueprint name appear twice:
1. As the Blueprint's root directory
2. Inside the templates directory

Know that by doing this, you avoid possible **template name collisions** between different Blueprints.

As a final note, it’s important to know that templates in the application’s template directory have greater precedence than those inside the Blueprint’s template directory. This can be useful to know if you want to override Flask Blueprint templates without actually modifying the template file.

to override the template products/view.html in the Products Blueprint:

```
ecommerce/
|
├── products/
|   └── templates/
|       └── products/
|           ├── search.html
|           └── view.html
|
└── templates/
        └── products/
            └── view.html
```

When you do this, your program will use `templates/products/view.html` instead of `products/templates/products/view.html` whenever a view requires the template `products/view.html`.

**Providing More than Views**

Flask Blueprint can also extend applications with **templates, static files, and template filters**. For example, you could create a Flask Blueprint to provide a set of icons and use it across your applications.

```
app/
|
└── icons/
    ├── static/
    |   ├── add.png
    |   ├── remove.png
    |   └── save.png
    |
    ├── __init__.py
    └── icons.py
```

The static folder contains the icon files and icons.py is the Flask Blueprint definition.

```
# icons.py
from flask import Blueprint

icons_bp = Blueprint('icons_bp', __name__,
    static_folder='static',
    static_url_path='icons')
```

* This code defines the icons_bp Flask Blueprint that exposes the files in the static directory under the /icons/ URL.
* When you can create Blueprints that package views and other types of content, you make your code and assets more reusable across your applications. 

### Summary

* A blueprint is a collection of views, templates, static files and other extensions that can be applied to an application.
* Blueprints are a great way to organize your application.
* In a divisional structure, each blueprint is a collection of views, templates and static files which constitute a particular section of your application.
* In a functional structure, each blueprint is just a collection of views. The templates are all kept together, as are the static files.
* To use a blueprint, you define it then register it on the application by calling `Flask.register_blueprint()`.
* You can define a dynamic URL prefix that will be applied to all routes in a blueprint.
* You can also define a dynamic subdomain for all routes in a blueprint.
* Refactoring a growing application to use blueprints can be done in five relatively small steps.

## References

1. [Explore Flask: Blueprints](https://exploreflask.com/en/latest/blueprints.html)
2. [Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/#why-blueprints)
3. [Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)
4. [How To Structure a Large Flask Application with Flask Blueprint and Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy)