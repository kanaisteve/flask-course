# Flask Login Tutorial

**What you'll learn:**
```
1. Package Installation
2. File Structure
3. Create Flask App
4. Add HTML Templates (Register, Login & Dashboard)
5. Database & User Model Setup
6. Forms
7. Signing Up, Logging In and Logging Out a User

```

**Dependencies:**
```
1. flask
2. flask_sqlalchemy
3. flask_login
4. flask_wtf
5. wtforms
6. flask_bcrypt
```

## 1. app.py

```
from flask import Flask, render_template, url_for, redirect
from flask flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
    
    # validate for similar user
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
    
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. Register Page

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login Page</h1>

    <form action="" method="POST">
        {{ form.hidden_tag() }}
        {{ form.username }}
        {{ form.password }}
        {{ form.submit }}
    </form>

    <a href="{{ url_for('register') }}">Don't have an account? Sign Up</a>
</body>
</html>

#### 2.1 Querying From Database:

```
>>> sqlite3 database.db
>>> select * from user;
```

## 3. Login Page

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login Page</h1>

    <form action="" method="POST">
        {{ form.hidden_tag() }}
        {{ form.username }}
        {{ form.password }}
        {{ form.submit }}
    </form>

    <a href="{{ url_for('register') }}">Don't have an account? Sign Up</a>
</body>
</html>
```

## 4. Dashboard Page

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <h1>Hello you are logged in.</h1>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
```

# References

1. [Python Flask Authentication Tutorial - Learn Flask Login](https://www.youtube.com/watch?v=71EU8gnZqZQ&list=PL0iII0bIwvpIUC7SwtR2l09jeEUbPr4-p&index=11)