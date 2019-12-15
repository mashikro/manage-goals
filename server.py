################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os

from model import connect_to_db, db, User, UserGoals






####################### RUNNING MY SERVER ###############################
if __name__ == "__main__":
   
    app.debug=False # We have to set debug=True here, since it has to be True at the point that we invoke the DebugToolbarExtension

    connect_to_db(app, "goals")

    DebugToolbarExtension(app) # Use the DebugToolbar

    app.run(host="0.0.0.0") 
