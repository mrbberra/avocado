# For running just the Flask server dyno, from the Procfile
from webserver import app
import os

if os.environ['DEBUG']:
    DEBUG = True
app.run(debug=DEBUG,use_reloader=False)
