from fabric import Connection, task
import random
import string
import os
from werkzeug.security import generate_password_hash

def generate_random_string(num_charachters):
    return ''.join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits,
        k=num_charachters))

def generate_command(password, debug, port):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    if password == '':
        password = generate_random_string(15)
    env_dict = {
        'SECRET_KEY': generate_random_string(30),
        'CSRF_KEY': generate_random_string(30),
        'ADMIN_PASS_HASH': generate_password_hash(password),
        'PORT': port,
        'PATH': os.environ['PATH'],
        'DATABASE_URL': 'sqlite:///' + os.path.join(base_dir, 'app.db')
    }
    if debug == 'True':
        env_dict['DEBUG'] = 'True'

    print('PLEASE RECORD YOUR ADMIN PASSWORD: ' + password)
    return env_dict

@task
def local(fabric_vars, password='', debug='True', port='5000'):
    env_dict = generate_command(password, debug, port)
    print('Starting server locally in debug mode at port ' + port + '.')
    start_string = 'gunicorn --timeout 6000 --bind localhost:' + port + ' run_all:app'
    with Connection('localhost') as c:
        c.local(start_string, env=env_dict)
