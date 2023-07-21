# File Upload With Flask

`$ pip install flask`

By the end, your project layout will look like this:
```
/home/user/Projects/flask-file-upload
|-- static/
|   |-- images
|-- templates/
|   |-- index.html
|-- venv
|-- main.py
```

```
# main.py
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # first grab the file
        file.save(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename) # save the file
        ))
    
    return render_template('index.html', form=form)


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
    <p>Flask File Upload Tutorial</p>
    
    <form method="POST" enctype="multipart/form">
        {{ form.hidden_tag() }}
        {{ form.file() }}
        {{ form.submit() }}
    </form>
</body>
</html>
```

# References

1. [How to Upload Files with Flask Using Python - YouTube](https://www.youtube.com/watch?v=GeiUTkSAJPs)