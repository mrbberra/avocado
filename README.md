## Required
- Python 3.6+
- virtualenv and virtualenvwrapper (highly suggested)
- Pip
- Appropriate [Selenium web driver](https://selenium-python.readthedocs.io/installation.html#drivers) for your choice of browser

## Installation
1. Clone the repo.
2. Make a new virtual environment
```
$ mkvirtualenv avocado
```
3. Run `pip install -r requirements.txt`

## Running the server in development
The server requires the following environment variables to be set:
- A hashed version of the admin password
- The port on which to run
- A Flask secret key
- A CSRF secret key
- Whether or not to run in debug mode

The fabfile can generate and set all of these.
- secret keys are always automatically generated
- the port defaults to 5000
- debug mode defaults to false
- the password can be configured or generated automatically
To use defaults, run the below command from within your virtual environment. The generated admin password will be printed to the shell:
```
$ fab local
PLEASE RECORD YOUR ADMIN PASSWORD: Z7Q9jZLvzjTslwB
Starting server locally in debug mode at port 5000.
```
The port, password, and debug mode are all configurable:
```
$ fab local --password=admin --port=8000 --debug=False
```

See the docs for [nose command line options](https://nose.readthedocs.io/en/latest/man.html)
