from tinydb import TinyDB, Query
from flask import request, url_for
from urllib.parse import urlparse, urljoin
from werkzeug.security import check_password_hash

class User():
    # only need one user
    def __init__(self):
        self.db = TinyDB('user_db.json')
        self.is_authenticated = self.check_auth()
        self.is_active = True
        self.is_anonymous = False
        self.password_hash = self.db.get(doc_id=len(self.db))['password_hash']

    def get_id(self):
        return len(self.db)

    def validate(self, username, password):
        if check_password_hash(self.password_hash, password) and username == 'admin':
            self.db.update({'authenticated': "True"}, Query().username == 'admin')
            return True
        else:
            print('test')
            return False

    def logout(self):
        self.db.update({'authenticated': "False"}, Query().username == 'admin')

    def check_auth(self):
        if 'True' == self.db.get(doc_id=len(self.db))['authenticated']:
            return True
        else:
            return False

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
