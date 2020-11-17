from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),nullable=False )
    email = db.Column(db.String(80), unique=True, nullable=False )
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }


class TodoList(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('users', lazy=True))

    def __init__(self, title,  user_id):
        
        self.title = title
        self.user_id = user_id

    def __repr__(self):
        return '<TodoList %r>' % self.title
    

    def todoListSerialize(self):
        return {
            'id': self.id, 
            'title': self.title,
            'user_id': self.user_id,   
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }


class Task(db.Model):

    __tablename__ = 'task_lists'
    id = db.Column(db.Integer, primary_key=True) 
    task_name = db.Column(db.String(80), nullable=False)
    task_body = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, nullable=False,)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)
    todo_lists = db.relationship('TodoList', backref=db.backref('todo_lists', lazy=True))

    def __init__(self, task_name, task_body, status, todo_id):
        
        self.task_name = task_name
        self.task_body = task_body
        self.status = status
        self.todo_id = todo_id

    def __repr__(self):
        return '<TodoList %r>' % self.task_name
    

    def todoListSerialize(self):
        return {
            'id': self.id, 
            'task_name': self.task_name,
            'task_body': self.task_body,
            'status': self.status,   
            'todo_id': self.todo_id,   
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
