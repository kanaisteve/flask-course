# Creating a Flask + React Project

In this tutorial, we learn how to set up flask as the backend and react as the frontend.

`$ pip install flask`

By the end, your project layout will look like this:
```
/home/user/Projects/flask-react
|-- client/
|   |-- node_modules
|   |-- public
|   |-- src
|       |-- App.css
|       |-- App.js
|       |-- index.js
|-- server/
|   |-- server.py
|   |-- venv
```

`$ mkdir server`

`$ cd server`

`$ touch server.py`

## 1. Creating the React App

Open up another terminal to create a react app.

### 1.1 Project setup with create-react-app
```
$ node -v
$ npm -v
$ npx create-react-app client
$ cd client
$ npm install
$ npm start
```

### 1.2 Project setup with Vite
```
# create vite + react app
$ npm create vite@latest client -- --template react
$ cd client
$ npm install
$ npm run dev
```

## 2. Backend - Virtual Environment & Package Installation 

## 2.1 Create an environment

### 2.1.1 Using Virtual Environment Folder

Create a project folder and a .venv folder within:

**1. MacOS**

`$ mkdir myproject`

`$ cd myproject`

`$ python3 -m venv .venv`


**2. Windows**

`> mkdir myproject`

`> cd myproject`

`> py -3 -m venv .venv`

#### Activate the environment

Before you work on your project, activate the corresponding environment:

**1. MacOS/Linux**

`$ . .venv/bin/activate`

**2. Windows**

`> .venv\Scripts\activate`

### 2.1.2 Pipenv

`$ cd flask_react/server`

`$ pipenv shell`

`$ pipenv install flask`


## 2.2 Install Flask

Before you work on your project, activate the corresponding environment:

`$ pip install flask Flask-SQLAlchemy python-dotenv`

-- or --

`$ pipenv install flask Flask-SQLAlchemy python-dotenv`

By default Flask will assume we running in production, we need to tell it we running in development:

`$ export FLASK_ENV=development`

## 3. Backend - Building the Backend API

```
from flask import Flask

app = Flask(__name__)

# members API route
@app.route('/members')
def members():
    return {"members": [
        "Member1",
        "Member2",
        "Member3"
    ]}


if __name__ == '__main__':
    app.run(debug=True)
```

## 4. Frontend Proxy Configuration and Setting Up

```
# client/src/App.js
import React, { useState, useEffect } from 'react'

function App() {
    const [data, setData] = useState([{}])
    
    # code fetch the api
    useEffect(() => {
        fetch('/members').then(
            res => res.jon()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])
    
    return(
        <div>
            {(type data.members === 'undefined') ? (
                <p>Loading...</p>
            ) : (
                data.memmbers.map((member, i) => (
                    <p key={i}>{member}</p>
                ))
            )}
        </div>
    )
}

export default App
```