# IMPORT LIBRARIES

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Creating App and Databse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)


# There are two Classes - Todo and Password. Todo Saves all meal-count and Password saves all Password

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = True)
    lunch = db.Column(db.String(500), nullable = True)
    desc2 = db.Column(db.String(500), nullable = True)
    dinner = db.Column(db.String(500), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


class Password(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    room = db.Column(db.String(500), nullable = True)
    Password = db.Column(db.String(500), nullable = True)


# Register Page

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method=='POST':
        password = request.form['password']
        room = request.form['room']
        passw = Password(room = room, Password = password)
        db.session.add(passw)
        db.session.commit()
        return redirect("/")
    return render_template('registration.html')

# Login Page

@app.route("/", methods = ['GET', 'POST'])
def login_user():
    if request.method=='POST':
        password = request.form['password']
        room = request.form['room']
        passw = Password.query.filter_by(room = room).first()
        if(passw.Password == password):
          title = request.form['room']
          desc = request.form['desc']
          desc2 = request.form['desc2']
          lunch = request.form['lunch']
          dinner = request.form['dinner']
          todo = Todo(title=title, desc=desc, desc2=desc2, lunch = lunch, dinner = dinner)
          db.session.add(todo)
          db.session.commit()
          return redirect("/home")
          
        
        

        
    
    return render_template('login.html')

# Home Page

@app.route("/home", methods = ['GET', 'POST'])
def hello_world():
   
    allTodo = Todo.query.all()
    allpass = Todo.query.all()
    return render_template('index.html', allTodo=allTodo, allpass = allpass)


# Update Page

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        desc = request.form['desc']
        desc2 = request.form['desc2']
        lunch = request.form['lunch']
        dinner = request.form['dinner']
        password = request.form['password']
        todo = Todo.query.filter_by(sno=sno).first()
        passw = Password.query.filter_by(room = todo.title).first()
        todo.desc = desc
        todo.desc2 = desc2
        todo.lunch = lunch
        todo.dinner = dinner
        if(password == passw.Password):
            db.session.add(todo)
            db.session.commit()
            return redirect("/home")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

# delete Route

@app.route("/delete/<int:sno>", methods = ['GET', 'POST'])
def delete(sno):
    if request.method=='POST':
        password = request.form['password']
        todo = Todo.query.filter_by(sno = sno).first()
        passw = Password.query.filter_by(room = todo.title).first()
        if(password == passw.Password):
            db.session.delete(todo)
            db.session.commit()
            return redirect("/home")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('delete.html', todo = todo)
# List Route

@app.route("/list/<int:sno>", methods = ['GET', 'POST'])
def show(sno):
    todo = Todo.query.filter_by(sno = sno).first()
 
    return render_template('list.html', todo = todo)



if __name__ == "__main__":
    app.run(debug=True, port=8000)  