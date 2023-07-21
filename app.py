# how to build a website with flask
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ktech20"
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # optional
app.permanent_session_lifetime = timedelta(minutes=30)
# app.permanent_session_lifetime = timedelta(days=30)

db = SQLAlchemy(app)
# initialize the app with the extension
# db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


with app.app_context():
    db.create_all()

# welcome page
@app.route('/')
def home():
    if "email" in session:
        email = session["email"]
    else:
        email = None

    python_projects = ["Python Training", "Web Development", "Automation Scripts", 
                       "Data Analysis Tools", "Chatbot Development", 
                       "Machine Learning Models", "Digital Marketing"]
    
    return render_template("index.html", projects=python_projects, email=email)

# learning page
@app.route('/learning')
def features():
    if "email" in session:
        email = session["email"]
    else:
        email = None

    return render_template("learning.html", email=email)

# login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True # increase timeout session to line 7
        # get variable values from form
        email = request.form["email"]
        # generate session
        session["email"] = email

        user = User.query.filter_by(email=email).first()

        if user is not None:
            flash("Login Successful!")
            return redirect(url_for("profile"))
            # return render_template("profile.html", username=username, email=email)
        else:
            flash("Invalid email or user does not exist.")
            return redirect(url_for("login"))
    else:
        if "email" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))
        
        return render_template("login.html")

# register page
@app.route('/register', methods=['POST', 'GET'])
def register():
    # create account with POST
    if request.method == "POST":
        session.permanent = True # increase timeout session to line 7
        # get variable values from form
        email = request.form["email"]
        username = request.form["username"]
        # password = request.form["password"]

        # validation
        if User.query.filter_by(email=email).first() is not None:
            flash("Email is taken!", category='error')
            return redirect(url_for("login"))
    
        if User.query.filter_by(username=username).first() is not None:
            flash("Username is taken!", category='error')
            return redirect(url_for("login"))
    
        # pwd_hash = generate_password_hash(password)

        # check if user exists and add user
        user = User.query.filter_by(email=email).first()
        if user:
            # generate sessions
            session["email"] = user.emai
            session["username"] = user.username
        else:
            # add new user
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()

        flash("Account Created Successful!")
        return redirect(url_for("profile"))
    
    # GET registration form
    else:
        if "email" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))
        
        return render_template("register.html")
    
# logout
@app.route('/logout')
def logout():
    flash("You have been logged out!", category='error')
    # pop out email session
    session.pop("username", None)
    session.pop("email", None)
    return redirect(url_for("login"))

# display user profile
@app.route('/profile', methods=["POST", "GET"])
def profile():

    if "email" in session:
        # retrieve email from session
        email = session["email"]

        # fetch user from database by email
        user = User.query.filter_by(email=email).first()

        if request.method == "POST":
            email = request.form["email"]
            username = request.form["username"]

            user.username = username
            user.email = email
            db.session.commit()
            # flash success message
            flash("Profile updated!", category='success')
        else:
            if "email" in session:
                email = session["email"]
                user = User.query.filter_by(email=email).first()

        return render_template("profile.html", email=email, username=user.username)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


# users list
@app.route('/users')
def users():
    if "email" in session:
        email = session["email"]
    else:
        email = None

    return render_template("users.html", users=User.query.all(), email=email)

# delete user
@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.delete()
    db.session.commit()
    return redirect(url_for("login"))

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

