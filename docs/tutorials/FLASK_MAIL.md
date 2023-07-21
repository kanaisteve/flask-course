# Sending Emails Using Flask-Mail

`$ pip install flask flask-mail`

By the end, your project layout will look like this:
```
/home/user/Projects/flask-mail
|-- static/
|-- templates/
|   |-- index.html
|-- venv
|-- main.py
```

```
# main.py
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)
# set up flask mail
mail = Mail(app)

# configure mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_SERVER'] = 'kanaistevew@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = Message("Hey", send='noreply@demo.com', recipients=['kanaistevew@gmail.com'])
        msg.body = "Hey how are you? Is everythin okay?"
        mail.send(msg)
        return "Sent email."
    
    return render_template('index.html')



if __name__ = '__main__':
    app.run(debug=True)
```

```
# templates/index
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Mail Tutorial</title>
</head>
<body>
    <p>Flask Mail Tutorial</p>
    
    <form method="POST">
        <button>Send email</button>
    </form>
</body>
</html>
```

# References

1. [How to Send Emails Using Flask - YouTube](https://www.youtube.com/watch?v=L7Cslucyyyo)