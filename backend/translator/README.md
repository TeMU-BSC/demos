# REST API with Flask

> REST API using [Flask](https://flask.palletsprojects.com/en/1.1.x/) microframework.

## Quick Start Using Pipenv

```bash
# Install pipenv tool
$ pip install pipenv

# Create a virtual environment inside project directory
$ export PIPENV_VENV_IN_PROJECT=1
$ pipenv --python 3.7

# [Development] Install dependencies with deterministic version listed in Pipfile.lock
$ pipenv install --dev

# [Production] Install dependencies with deterministic version listed in Pipfile.lock
$ pipenv install --deploy

# Activate virtual environment with pipenv
$ pipenv shell

# Run Server
$ export FLASK_APP=translator.py
$ flask run
```

## Accepted HTTP Verbs and API Routes

- GET /samples
- POST /translate

## JSON Response Structure

```
{
  success: boolean,
  data: any,
  message: string
}
```
