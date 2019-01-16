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
    if password == '':
        password = generate_random_string(15)
    env_dict = {
        'SECRET_KEY': generate_random_string(30),
        'CSRF_KEY': generate_random_string(30),
        'ADMIN_PASS_HASH': generate_password_hash(password),
        'PORT': port,
        'GOOGLE_CHROME_SHIM': '/usr/bin/google-chrome',
        'PATH': os.environ['PATH']
    }
    if debug == 'True':
        env_dict['DEBUG'] = 'True'

    print('PLEASE RECORD YOUR ADMIN PASSWORD: ' + password)
    return env_dict

@task
def local(fabric_vars, password='', debug='True', port='5000'):
    env_dict = generate_command(password, debug, port)
    print('Starting server locally in debug mode at port ' + port + '.')
    with Connection('localhost') as c:
        c.local('echo $PYTHONPATH', env=env_dict)
        c.local('python run.py', env=env_dict)
