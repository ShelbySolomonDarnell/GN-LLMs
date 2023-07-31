# GN-LLMs
Writing and code for large language models to be used with GeneNetwork.org


## How To Run

This is based on: [flask-pixel](https://github.com/app-generator/flask-pixel)

### Using GNU Guix

Make sure that you are using the latest channels file provided in our CI [here](https://ci.genenetwork.org/channels.scm).

```sh
cd flax-pixel/
env FLASK_APP=run.py FLASK_ENV=development ASSETS_ROOT=~/projects/GN-LLMs/flask-pixel/apps/static/assets/ flask run
```

Update the path to the `ASSETS_ROOT` as suitable

Also, update the path to you API config in *.apps/apihandler/process.py*.

## How to Run the Material-Flask version of the  site (preferred)

For more information about material flask, look at the [readme in the material-flask](/material-flask/README.md) directory.

### Using GNU Guix
Make sure that you are using the latest channels file provided in our CI [here](https://ci.genenetwork.org/channels.scm).

Also, update the path to you API config in *.apps/apihandler/process.py*.

```sh
cd material-flask/
./run_guix-shell.sh
```

The site should be up at localhost:5005

### Using Docker
The nginx configuration file needs to be modified for the docker container to work correctly.
```
cd material-flask/nginx
mv matflask-app.old matflask-app.conf
cd ../..
docker build . -t matflask_app
docker-compose up
```
The site should be up at localhost:5095.
