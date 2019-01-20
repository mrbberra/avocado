## About
This is a work-in-progress site to visualize the data from https://twitter.com/hpavocadoprice.
Tweets are downloaded using Selenium, checking for new posts every 5 minutes. Prices are manually updated by the site maintainers via an admin interface. The site is currently deployed at https://avocado-prices.herokuapp.com. The visualization is in progress, but the data is available at /data and /data/<tweet_id>, for any <tweet_id> listed in /data.

## Required
- Python 3.6+
- virtualenv and virtualenvwrapper (highly suggested)
- Pip
- Postgres, available at the project [website](https://www.postgresql.org/) or from a package manager like [brew](https://brew.sh/).
- Appropriate [Selenium web driver](https://selenium-python.readthedocs.io/installation.html#drivers) for your choice of browser.
  - Web drivers can also be installed using brew.
  - Currently, this project uses Chrome for compatibility with Heroku. If you wish to use something else, you will have to modify the TweetFetcher __init__ statement.

## Installation
1. Clone the repo.
2. Make a new virtual environment
```
$ mkvirtualenv avocado
```
3. Run `pip install -r requirements.txt`
4. Create the postgres database
```
createdb <db_name>
```

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
