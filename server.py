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
    '''Index. User can either go to 'create an account' or 'login' page '''
    
    return render_template('index.html') 

@app.route('/create-account', methods=['GET']) 
def create_account():
    '''Create Account page. '''
    
    return render_template('create_account.html') 

@app.route('/login', methods=['GET']) 
def login_user():
    '''Login page. '''
    
    return render_template('login.html') 

@app.route('/create-account', methods=['POST'])
def create_user_process():
    '''Add user to the database'''

# Will get all this info back:
    email = request.form.get('email')
    password = request.form.get('password')
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

@app.route('/home', methods=['GET'])
def show_homepage():
    '''Homepage. Users can add a goal here'''

    user_id = session.get('user_id')

    if user_id:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/home', methods=['POST'])
def process_goal():
    '''Process user's goals and save in backend'''

    goal_text = request.form.get('goal_text')

    new_goal = UserGoals(user_id = session['user_id'],
                        goal_text = goal_text)


    db.session.add(new_goal)
    db.session.commit()

    return redirect('/history')

@app.route('/history', methods=['GET'])
def show_history_page():
    '''History page. Users can view all their goals here'''

    user_id = session.get('user_id')

    user_goals = UserGoals.query.filter_by(user_id=user_id)

    if user_id:
        return render_template('history.html', 
                                user_goals=user_goals)

    else:
        return redirect('/')

@app.route('/edit-goal/<int:goal_id>')
def edit_goal(goal_id):

    goal_to_edit=UserGoals.query.filter_by(goal_id=goal_id).first()

    return render_template('edit_goal.html', goal_to_edit=goal_to_edit)

@app.route('/edit-goal/<int:goal_id>', methods=['POST'])
def edit_goal_process(goal_id):
    '''Change goal in db'''

    new_goal = request.form.get('new_goal')

    print('NEWWW GOALLLLL', new_goal)

    goal_to_edit=UserGoals.query.filter_by(goal_id=goal_id).first()

    goal_to_edit.goal_text = new_goal

    db.session.commit()

    return redirect('/history')

#each goal will have an edit link (like details link from project)
#in that link users will fill our a form which I will process based on goal id
#in the db i will update the 

####################### RUNNING MY SERVER ###############################
if __name__ == "__main__":
   
    app.debug=True # We have to set debug=True here, since it has to be True at the point that we invoke the DebugToolbarExtension

    connect_to_db(app, "goals")

    DebugToolbarExtension(app) # Use the DebugToolbar

    app.run(host="0.0.0.0") 
