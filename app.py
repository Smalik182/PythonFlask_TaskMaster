from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# To activate our enviroment: .\env\Scripts\activate in the terminal

# for error "cannot be loaded because running scripts is disabled on this system"
# run: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted, in terminal



# Set up the application and reffernece the name
app = Flask(__name__)

# Tell our database where our app is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initialize our database
db = SQLAlchemy(app)


# Here we create our model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)      # an integer that refferences the id of each task
    content = db.Column(db.String(200), nullable=False) # String of up to 200 chars, nullable = false because we dont want the user to leave it blank
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  #anytime a new entry is created, date and time is auto set

    # function to return a string everytime we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id


# Create an idex route so that when we browse to the url we don't immediately 404
# you set up routes in Flask with the app.route decorator
@app.route('/', methods = ['POST', 'GET'])

# Define function for that route
def index():
    if request.method == 'POST':
        task_content =request.form['content']   # logic for adding a task, form we created in index.html
        new_task = Todo(content = task_content) # todo object, that will have the contents = task_content

        # Here we try to push to our database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()    # looks at all database contents created and returnds all of themm
        return render_template('index.html', tasks = tasks)


# Delete route for our database
@app.route('/delete/<int:id>')          # We delete through the int ID in Todo
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)      # attempt to get the task by that id, if it doesn't work, 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'


# Update route for our database
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect ('/')
        except:
            return 'There was issue updating the task'
    else:
        return render_template('update.html', task=task)

# Template Inheiritence: You create one master html  file that contains the skeleton of what each page will look
# like and you just inheirit that in each other page

if __name__ == "__main__":
    app.run(debug=True)

