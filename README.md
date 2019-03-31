# docker-volume-nest

Manage volumes for a simple docker swarm deploy

This project its heavily based on [https://github.com/ronin13/pyvolume]

## Command line

docker-volume-nest comes with a command line interface. See help for more information:

See `docker_volume_nest --help`

## Install

Install the debian package using:

    apt-get install docker_volume_nest

## Development

From the root of the application directory, create a python environment,
install the application in development mode along with its dependencies and
run it locally:

    virtualenv env
    . env/bin/activate
    pip install --upgrade pip
    pip install -e . -r requirements.txt -r dev-requirements.txt

Tests can be run using *tox* (recommended):

    pip install tox
    tox

Or directly by calling *py.test*:

    python -m pytest
