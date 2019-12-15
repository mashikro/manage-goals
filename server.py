################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os

from model import connect_to_db, db, User, UserGoals

#################### FLASK APP SET-UP ####################################
app = Flask(__name__)

app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined #to prevent silent but deadly jinja errors

######################### ROUTES #####################################
@app.route('/') 
def index():
    '''Index. User can either 'create an account' or 'login here' '''
    
    return render_template('index.html') 


@app.route('/create-account', methods=['POST'])
def create_user_process():
    '''Add user to the database'''

# Will get all this info back:
    email = request.form.get('email')
    password_hash = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
   

#checks if a user w that email already exists, if 'True' redirects them to try again.
    user = User.query.filter_by(email=email).first()

    if user:
        flash('''Sorry this email is already being used. 
            Try again with a different email address.''')
        
        return redirect('/')
    
#Instatitate a new user add and commit them to db
    new_user = User(email=email, 
                    password=password, 
                    fname=fname, 
                    lname=lname)

    db.session.add(new_user)
    db.session.commit()
 
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_process():
    '''Authenticate user'''

# Will get this info back
    email = request.form.get('email')
    password = request.form.get('password')

# Will query for the user with this email (emails are unique)
    user = User.query.filter_by(email=email).first()

#User authentication
    if not user:
        flash("Sorry, the user with that email doesn't exist. Please try again :) ")
        return redirect('/')
   
    if password == user.password: #this checks if the entered pass matches pass in db
       
        #add user to session
        session['user_id'] = user.user_id

        # Will have a flash message
        flash('Welcome! We missed you <3')

        return redirect('/home')
    
    # if pass doesnt match:
    else:
        flash('Oops :0 Incorrect password! Please try again :)')
        return redirect('/')


#each goal will have an edit link (like details link from project)
#in that link users will fill our a form which I will process based on goal id
#in the db i will update the 

####################### RUNNING MY SERVER ###############################
if __name__ == "__main__":
   
    app.debug=False # We have to set debug=True here, since it has to be True at the point that we invoke the DebugToolbarExtension

    connect_to_db(app, "goals")

    DebugToolbarExtension(app) # Use the DebugToolbar

    app.run(host="0.0.0.0") 
