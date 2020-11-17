from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import model
from model import todolist
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///example.sqlite"
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def hello():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        db_password =  model.check_password(username)
        if password == db_password:
            message =  model.show_color(username)
            return render_template('index.html', message = message)
        else:
            error_message = 'Hint : He curse a lot'
            return render_template('index.html', message = error_message)


@app.route('/about', methods=["GET" ])
def about():
    return render_template('about.html')

@app.route('/privacy', methods=["GET" ])
def privacy():
    return render_template('privacy.html')

@app.route('/terms', methods=["GET"])
def terms():
    return render_template('terms.html')






@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]
        if not password and not email:
            user_info = model.login (email,password)
            todolist = model.todolist(user_info['pk'])
            return render_template('dashboard.html',user_info =user_info, todolist =todolist )
        else:
            message = "please fill all input"
        return  render_template('login.html', message = message)
        













@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password == confirm_password:

            message = model.signup(username,password)
            
        else:

            message = "Password does not match"
            
        return render_template('signup.html', message = message)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run(port=8000, debug=True,)