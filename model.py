############## CREATING TO DATABASE ############################
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# from collections import defaultdict

db = SQLAlchemy()

#################### MODEL DEFINITIONS ##########################

class User(db.Model):
    '''All user and user info will live here'''
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False )
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique= True, nullable=False)
    password = db.Column(db.Text, nullable=False) #store password non securely


    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<User: email-{email} fname-{fname}>'.format(email=self.email, 
                                                            fname=self.fname)

class UserGoals(db.Model):
    '''All user and user info will live here'''
    __tablename__ = 'user_goals'
   
    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    goal_text = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref='journal_entries') #one to many relationship User can have many Goals.

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<user_email-{user_email} goal_text-{goal_text}>'.format(user_email=self.user.email, 
                                                            goal_text=self.goal_text)

################# DB SET UP #########################
def connect_to_db(app, dbname):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app 

    connect_to_db(app, "goals")
    print("Connected to DB.")
