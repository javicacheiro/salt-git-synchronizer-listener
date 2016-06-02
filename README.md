
Installation
------------

```
cd bigdata/git_synchronizer_listener/
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

```

Running
-------

Running the application in production using screen:
```
screen
su - gitsync
cd bigdata/git_synchronizer_listener/
. venv/bin/activate
FLASK_CONFIG=production gunicorn --workers=2 --bind=:5000 wsgi:application

```

Usage
-----

Populate the state saltenvs
```
curl -X POST -H "Content-Type: application/json" -d '{ "name": "master" }' http://localhost:5000/git/v1/saltenvs/states
curl -X POST -H "Content-Type: application/json" -d '{ "name": "testing" }' http://localhost:5000/git/v1/saltenvs/states
```

NOTICE: The base saltenv is mapped to the master git branch and to simplify the implementation it is named master

Populate the pillar saltenvs
```
curl -X POST -H "Content-Type: application/json" -d '{ "name": "master" }' http://localhost:5000/git/v1/saltenvs/pillars
curl -X POST -H "Content-Type: application/json" -d '{ "name": "testing" }' http://localhost:5000/git/v1/saltenvs/pillars
```

Get available state saltenvs
```
curl http://localhost:5000/git/v1/saltenvs/states
```

Get available pillar saltenvs
```
curl http://localhost:5000/git/v1/saltenvs/pillars
```

See when a the master (base) state saltenv was updated
```
curl http://localhost:5000/git/v1/saltenvs/states/master
```

Synchronize a given state saltenv with the git remote repo:
```
curl -X PUT http://localhost:5000/git/v1/saltenvs/states/master
```

