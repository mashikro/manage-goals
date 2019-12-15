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
    password_hash = db.Column(db.Text, nullable=False) #store password non securely


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

        return '<User: email-{email} fname-{fname}>'.format(email=self.email, 
                                                            fname=self.fname)

