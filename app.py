import os
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#to show the database in drectory

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'todo.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db=SQLAlchemy(app)
db.init_app(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    time_todo = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# to create the database

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        time_todo = request.form['time_todo']
        todo = Todo(title=title,desc = desc,time_todo = time_todo)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo = allTodo)

    
@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        time_todo = request.form['time_todo']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")  
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)    

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    

if __name__=="__main__":
    app.run(debug=True)    