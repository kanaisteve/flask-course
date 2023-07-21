# User Authentication in Flask App Using JWT [JSON Web Token]

`pip install flask flask-jwt-extended functools`

## 1. ways to generate a secret_key for your flask app

```
# ways to generate a secret_key for your flask app
# 1. use urandom()
import os
os.urandom(12)
```

```
b'\x02\x06F\xbbC\xeeG\xe4@\xd2-^'
```

From the above output, you can use the generated string `\x02\x06F\xbbC\xeeG\xe4@\xd2-^` as the secret key for your flask application

```
# 2. use secret [comes with python 3.6+]
import secrets
secrets.token_urlsafe(12)
```

OUTPUT:
```
'i4TKkEWT_AfUhSvt'
```

```
# 3. uuid [make sure to install this package because its an external package]
import uuid
uuid.uuid4().hex
```

```
'77b820091b1b43a388e2c04c787e4b09'
```

## 2. app.py

### 2.1 Tutorial 1: User Authentication

```
# app.py
from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from funtools import wraps

app.Flask(__name__)
app.config['SECRET_KEY'] = '77b820091b1b43a388e2c04c787e4b09'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request/args.get('token')
        if not token:
            return jsonify({'Alert': 'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert': 'Invalid Token!'})
        
    return decorated

# home route
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'

# public
@app.route('/public')
def public():
    return 'For Public'

# authenticated
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'

# login
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == 'password23':
        session['logged_in'] = True
        
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: Authentication Failed'})
```

### 2.2 Tutorial 2: Authenticating a Flask API

```
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #https: //127.0.0.1:5000/route?token=q0wriwe09r09r4er90wier9
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        
        return f(*args, **kwargs)

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization
    
    # if user is authenticated, generate a token
    if auth and auth.password == 'password':
        token = jwt.encode({
            'user' : auth.username, 
            'exp' : datetime.datetime.utnow() + datetime.timedelta(minutes=30)
        },app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)
```

### 2.3 Tutorial 3: User Auth with Flask JWT Extended

JWT Extension in its simplest form is:
```
1. You use create_access_token() to make JSON Web Tokens, 
2. jwt_required() to protect routes, and 
3. get_jwt_identity() to get the identity of a JWT in a protected route.
```

User authentication using JSON Web Tokens (JWT) in a Flask app involves the following steps:

```
1. Install Required Packages
2. Configure Flask App
3. Create a User Login Endpoint
4. Protect Endpoint
5. Run app
```

#### 2.3.1. Install Required Packages:

Install the Flask package: pip install Flask
Install the Flask-JWT-Extended package: `pip install flask-jwt-extended`

#### 2.3.2. Configure Flask App:

```
# Import necessary modules:
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Create a Flask app instance:
app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'your_secret_key' 
jwt = JWTManager(app)
```

#### 2.3.3 Configure Flask App:

Define a route for user login, where the user provides credentials (e.g., username and password):

```
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Add authentication logic here to verify the user credentials
    # For example, check if the username and password match a user in your database

    if username == 'valid_user' and password == 'valid_password':
        access_token = create_access_token(identity=username)  # Generate JWT access token
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
```

#### 2.3.3 Protect Endpoint

Define a protected route that requires authentication using the jwt_required decorator:

```
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route('/protected', methods=['GET'])
@jwt_required()  # Require authentication for this endpoint
def protected():
    current_user = get_jwt_identity()  # Get the identity (username) from the JWT
    return jsonify({'message': f'Protected endpoint accessed by {current_user}'}), 200
    # return jsonify(logged_in_as=current_user), 200
```

To access a jwt_required protected view you need to send in the JWT with each request. By default, this is done with an authorization header that looks like:

`Authorization: Bearer <access_token>`


```
$ http GET :5000/protected

HTTP/1.0 401 UNAUTHORIZED
Content-Length: 39
Content-Type: application/json
Date: Sun, 24 Jan 2021 18:09:17 GMT
Server: Werkzeug/1.0.1 Python/3.8.6

{
    "msg": "Missing Authorization Header"
}


$ http POST :5000/login username=test password=test

HTTP/1.0 200 OK
Content-Length: 288
Content-Type: application/json
Date: Sun, 24 Jan 2021 18:10:39 GMT
Server: Werkzeug/1.0.1 Python/3.8.6

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxMTUxMTgzOSwianRpIjoiMmI0NzliNTQtYTI0OS00ZDNjLWE4NjItZGVkZGIzODljNmVlIiwibmJmIjoxNjExNTExODM5LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsImV4cCI6MTYxNDEwMzgzOX0.UpTueBRwNLK8e-06-oo5Y_9eWbaN5T3IHwKsy6Jauaw"
}


$ export JWT="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxMTUxMTgzOSwianRpIjoiMmI0NzliNTQtYTI0OS00ZDNjLWE4NjItZGVkZGIzODljNmVlIiwibmJmIjoxNjExNTExODM5LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsImV4cCI6MTYxNDEwMzgzOX0.UpTueBRwNLK8e-06-oo5Y_9eWbaN5T3IHwKsy6Jauaw"


$ http GET :5000/protected Authorization:"Bearer $JWT"

HTTP/1.0 200 OK
Content-Length: 24
Content-Type: application/json
Date: Sun, 24 Jan 2021 18:12:02 GMT
Server: Werkzeug/1.0.1 Python/3.8.6

{
    "logged_in_as": "test"
}
```

**Important**

Remember to change the `JWT secret key` in your application, and ensure that it is secure. The JWTs are signed with this key, and if someone gets their hands on it they will be able to create arbitrary tokens that are accepted by your web flask application.

#### 2.3.4 Run app

Add the following code at the bottom of your script to run the app:

```
if __name__ == '__main__':
    app.run()
```

### 2.4 Tutorial 4: Automatic User Loading¶

In most web applications it is important to have access to the user who is accessing a protected route. JWT provides a couple callback functions that make this seamless while working with JWTs.

The first is `user_identity_loader()`, which will convert any User object used to create a JWT into a JSON serializable format.

On the flip side, you can use `user_lookup_loader()` to automatically load your User object when a JWT is present in the request. The loaded user is available in your protected routes via `current_user`.

Lets see an example of this while utilizing SQLAlchemy to store our users:

### 2.4.1 app.py

```
# Import necessary modules:
from hmac import compare_digest

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.Text, nullable=False)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        return compare_digest(password, "password")


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )


if __name__ == "__main__":
    db.create_all()
    db.session.add(User(full_name="Bruce Wayne", username="batman"))
    db.session.add(User(full_name="Ann Takamaki", username="panther"))
    db.session.add(User(full_name="Jester Lavore", username="little_sapphire"))
    db.session.commit()

    app.run()
```

### 2.4.2 Test Endpoints
Let's see this in action:

```
$ http POST :5000/login username=panther password=password

HTTP/1.0 200 OK
Content-Length: 281
Content-Type: application/json
Date: Sun, 24 Jan 2021 17:23:31 GMT
Server: Werkzeug/1.0.1 Python/3.8.6

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxMTUwOTAxMSwianRpIjoiNGFmN2ViNTAtMjk3Yy00ZmY4LWJmOTYtMTZlMDE5MWEzYzMwIiwibmJmIjoxNjExNTA5MDExLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTQxMDEwMTF9.2UhZo-xo19NXaqKLwcMz0NBLAcxxEUeK4Ziqk1T_9h0"
}


$ export JWT="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxMTUwOTAxMSwianRpIjoiNGFmN2ViNTAtMjk3Yy00ZmY4LWJmOTYtMTZlMDE5MWEzYzMwIiwibmJmIjoxNjExNTA5MDExLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTQxMDEwMTF9.2UhZo-xo19NXaqKLwcMz0NBLAcxxEUeK4Ziqk1T_9h0"


$ http GET :5000/who_am_i Authorization:"Bearer $JWT"

HTTP/1.0 200 OK
Content-Length: 57
Content-Type: application/json
Date: Sun, 24 Jan 2021 17:31:34 GMT
Server: Werkzeug/1.0.1 Python/3.8.6

{
    "id": 2,
    "full_name": "Kanai Wamulwange",
    "username": "kanaitech"
}

```

# References

1. [JWT.io](https://jwt.io/)
2. [User Authentication in Flask App Using JWT [JSON Web Token] - YouTube](https://www.youtube.com/watch?v=_3NKBHYcpyg)
3. [Authenticating a Flask API Using JSON Web Token - YouTube](https://www.youtube.com/watch?v=J5bIPtEbS0Q)
4. [Flask-JWT-Extended: Installation](https://flask-jwt-extended.readthedocs.io/en/stable/installation.html)
5. [Flask-JWT-Extended: Basic Usage](https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html)
6. [Flask-JWT-Extended: Automatic User Loading](https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading.html)