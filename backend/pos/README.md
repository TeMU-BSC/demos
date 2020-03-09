# REST API with Flask

> REST API using [Flask](https://flask.palletsprojects.com/en/1.1.x/) microframework.

## Quick Start Using Pipenv

``` bash
# Install pipenv tool
$ pip install pipenv

# Install requried dependencies listed in Pipfile
$ pipenv install

# Activate virtual environment with pipenv
$ pipenv shell

# Run Server
$ flask run
```

## Accepted HTTP Verbs and API Routes

* GET   /samples
* POST  /analyze

## JSON Response Structure

```
{
  success: boolean,
  data: any,
  message: string
}
```
