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
