from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# To activate our enviroment: .\env\Scripts\activate in the terminal



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
@app.route('/')

# Define function for that route
def index():
    return render_template('index.html')
# Template Inheiritence: You create one master html  file that contains the skeleton of what each page will look
# like and you just inheirit that in each other page

if __name__ == "__main__":
    app.run(debug=True)

