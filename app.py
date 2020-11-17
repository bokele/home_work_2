from os import error
from flask import Flask, render_template, request, redirect,session, g, flash, jsonify
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

import os




app = Flask(__name__)

app.secret_key = "Test@Bokele#$%^&*^#HJIKKLASKJaksNKQ!@@!&"

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from model import User, TodoList, Task


@app.route('/', methods=["GET"])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/about', methods=["GET" ])
def about():
    return render_template('about.html')

@app.route('/privacy', methods=["GET" ])
def privacy():
    return render_template('privacy.html')

@app.route('/terms', methods=["GET"])
def terms():
    return render_template('terms.html')

@app.route('/dashboard', methods=["GET"])
def dashboard():
    if request.method == 'GET':
        user_id = session['user_id']
        todoList = TodoList.query.filter_by(user_id = user_id).all()
        return render_template('dashboard.html',  todoList=todoList)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        if  password !="" and  email !="":
            user = User.query.filter_by(email=email, password = password).first()
            #user = User(email = email, password = password).first()
            if user:
                user_info =  user.serialize()
                session.clear()
                session['user_id'] =user_info['id']
                session['email'] =user_info['email']
                session['username'] =user_info['name']
                session['created_at'] =user_info['created_at']
                return redirect(url_for('dashboard'))
            else:
                message = "Incorrect email or password"
                return  render_template ('login.html', message = message) 
        else:
            message = "please fill all input"
            return  render_template ('login.html', message = message)
    return  render_template ('auth/login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('created_at', None)
    
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        # json.dumps(data)
        name=data['name']
        password=data['password']
        confirm_password=data['confirm_password']
        email=data['email']
        if password == confirm_password:
            user_exist =  User.query.filter_by(email=email).first()
            if user_exist is None:
                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                # return {"message": f"car {user.name} has been created successfully."}
                return  redirect(url_for('dashboard'))
            else:
                message = "This email is alread taken {}".format(email)
                return  render_template('register.html', message = message)
        else:
            message = "Password don't match"
            return  render_template('register.html', message = message)
       
    elif request.method == 'GET':
        return  render_template('auth/register.html')

    return  render_template('auth/register.html')


@app.route('/todo/create', methods=['POST', 'GET'])
def createTodo():
    if request.method == 'GET':
        success = ''
        return render_template('todo/create.html', success=success) 
    elif request.method == 'POST':
        data = request.form
        title=data['title']
       
       
        error = None
        if not title:
            error = "Title required"
            success = 'fasle'
        if error is None:
            user_id = session['user_id']
            todolist = TodoList(title=title, user_id=user_id)
            db.session.add(todolist)
            db.session.commit()
            message = "Your doTo list has been created"
            success = 'true'
            return render_template('todo/create.html', message = message, success = success) 
        else:
            success = 'fasle'
            return render_template('todo/create.html', error = error, success = success) 
        
    return render_template('todo/create.html') 

    

@app.route('/todo/delete', methods=['POST'])
def todolistDelete():
    if request.method == 'POST':
        data = request.form
        todolist_id = data['todo_id']   
        todoListiItem = TodoList.query.filter_by(id = todolist_id).first()
        db.session.delete(todoListiItem)
        db.session.commit()
        allTask = Task.query.filter_by(todo_id = todolist_id).all()
        db.session.delete(allTask)
        db.session.commit()
        flash('Todo and task have been deleted')
        return  redirect(url_for('dashboard'))

@app.route('/todolist/edit/<todolist_id>', methods=['POST', 'GET',])
def todolist(todolist_id):
    todoListiItem = TodoList.query.filter_by(id = todolist_id).first()


    response = todoListiItem.todoListSerialize()
    if request.method == 'GET':
        
        return render_template('todo/edit.html', todo_data = response) 

    elif request.method == 'POST':
        data = request.form
        title=data['title']
       
        error = None
        if not title:
            error = "Title required"
       

        if error is None:
            user_id = session['user_id']
            todolist = dict(title=title, user_id=user_id)
            TodoList.query.filter_by(id = todolist_id).update(todolist)
            db.session.commit()
            message = "Your doTo list has been updated"
            success = 'true'
            flash(message, success)
            return redirect(url_for('dashboard'))
        return render_template('todo/edit.html', todo_data = response, error =error) 


@app.route('/todolist/add/task/<todo_id>', methods=['POST', 'GET'])
def addTask(todo_id):
    if request.method == 'GET':
        success = ''
        return render_template('task/add-task.html', success=success, todo_id=todo_id) 
    elif request.method == 'POST':
        data = request.form
        task_name=data['task_name']
        task_body=data['task_body']
        status=data['status']
        error = None
        if not task_name:
            error = "Task Name required"
            success = 'fasle'
        if not status:
            error = "Status required"
            success = 'fasle'
        if error is None:
            if status == 'true':
                status = True
            else:
                status = False
            todo_id = todo_id
            task = Task(task_name=task_name, task_body=task_body, status=status, todo_id=todo_id)
            db.session.add(task)
            db.session.commit()
            message = "Your task has been added"
            success = 'true'
            return render_template('task/add-task.html', message = message, success = success) 
        else:
            success = 'fasle'
            return render_template('task/add-task.html', error = error, success = success) 
        
    return render_template('task/add-task.html') 

@app.route('/todolist/view/task/<todo_id>', methods=['GET'])
def viewTodoList(todo_id):
    
    if request.method == 'GET':
        todoListTask= Task.query.filter_by(todo_id = todo_id).all()
        return render_template('todo/detail.html', todoListTask = todoListTask)
   
@app.route('/task/delete/<todo_id>', methods=['POST'])
def deleteTask(todo_id):
    if request.method == 'POST':
        data = request.form
        task_id = data['task_id']   
        task = Task.query.filter_by(id = task_id).first()
        db.session.delete(task)
        db.session.commit()
        
        message = "Task has been deleted"
        success = 'true'
        flash(message, success)
        return redirect(url_for('viewTodoList',todo_id=todo_id))

@app.route('/task/edit/<task_id>', methods=['POST', 'GET'])
def editTask(task_id):
    task = Task.query.filter_by(id = task_id).first()
    response = task.todoListSerialize()
    if request.method == 'GET':
        return render_template('task/edit-task.html', task_data = response) 

    elif request.method == 'POST':
        data = request.form
        task_name=data['task_name']
        task_body=data['task_body']
        status=data['status']
        todo_id=data['todo_id']
        error = None
        if not task_name:
            error = "Task Name required"
            success = 'fasle'
        if not status:
            error = "Status required"
            success = 'fasle'
        if error is None:
            if status == 'true':
                status = True
            else:
                status = False
    
            user_id = session['user_id']
            task = dict(task_name=task_name, task_body=task_body, status=status, todo_id=todo_id)
            Task.query.filter_by(id = task_id).update(task)
            db.session.commit()
            message = "Your Task  has been updated"
            success = 'true'
            flash(message, success)
            return redirect(url_for('viewTodoList',todo_id=todo_id))
        return render_template('task/edit-task.html', todo_data = response, error =error) 
      

def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()





        