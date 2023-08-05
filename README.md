# GN-LLMs
Writing and code for large language models to be used with GeneNetwork.org


## How To Run

For more information about material flask, look at the [readme in the material-flask](/material-flask/README.md) directory.

### Using GNU Guix
Make sure that you are using the latest channels file provided in our CI [here](https://ci.genenetwork.org/channels.scm).

Update the path to the `ASSETS_ROOT` as suitable

Also, update the path to you API config in *.apps/apihandler/process.py*.

```sh
cd material-flask/
./run_guix-shell.sh
```

To run and keep track of output and errors, the command changes too

```sh
cd material-flask/
./run_guix-shell.sh > out.log 2> out2.log
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
