from fabric import Connection, task
import random
import string
import os
import time
from werkzeug.security import generate_password_hash

def generate_random_string(num_charachters):
    return ''.join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits,
        k=num_charachters))

def generate_env(password, debug, port):
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

@task(optional=['password', 'debug', 'port'])
def local(fabric_vars, password='', debug='True', port='5000'):
    env_dict = generate_env(password, debug, port)
    print('Starting server locally in debug mode at port ' + port + '.')
    start_string = 'gunicorn --timeout 6000 --bind localhost:' + port + ' run_all:app'
    with Connection('localhost') as c:
        c.local(start_string, env=env_dict)

@task(optional=['port'])
def test(fabric_vars, port='5000'):
    password = 'testing_password'
    debug = 'True'
    env_dict = generate_env(password, debug, port)
    env_dict['PASSWORD'] = password

    print('Starting server locally in debug mode at port ' + port + '.')
    start_string = 'gunicorn --daemon --timeout 6000 --bind localhost:' + port + ' run_all:app'
    site_test_string = 'pytest --driver Chrome --host 127.0.0.1 --port ' + port + ' webserver/test/site_test.py'
    tweet_test_string = 'pytest webserver/test/tweet_test.py'
    with Connection('localhost') as c:
        c.local(tweet_test_string, env=env_dict)
        c.local(start_string, env=env_dict)
        time.sleep(2)
        c.local(site_test_string, env=env_dict)
        c.local('pkill gunicorn')
