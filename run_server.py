# For running just the Flask server dyno, from the Procfile
from webserver import app
import os

if os.environ['DEBUG']:
    DEBUG = True
if __name__ == '__main__':
    app.run(debug=DEBUG,use_reloader=False)
