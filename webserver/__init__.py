# Import flask and template operators
from flask import Flask

# Import SQLAlchemy, CSRFProtect
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
csrf = CSRFProtect(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
#from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
#app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()