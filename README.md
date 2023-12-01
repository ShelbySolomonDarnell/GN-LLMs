# GN-LLMs
Writing and code for large language models to be used with GeneNetwork.org

For more information about material flask, look at the [readme in the material-flask](/material-flask/README.md) directory.

## Configuration

The recommended way to pass application settings is by passing the configuration parameters directly through the `env` command:


```sh
env ASSETS_ROOT=ASSETS_ROOT="/static/assets" \
	SECRET_KEY="our-little-secret" \
	SQLITE_URI="sqlite:///gnqa-db.sqlite3" \
	...
```

Alternatively, you could set the above paramaters via a configuration file that is sourced from the terminal e.g.

```sh
source ${HOME}/genenetwork/configs/GN_LLM_CONF
```

The configuration file should contain the following entries:

`**`sh
export ASSETS_ROOT="/static/assets"
export SECRET_KEY="our-little-secret"
export SQLITE_URI="sqlite:///gnqa-db.sqlite3"
`****

Ensure that each configuration parameter is appropriately set, either through the dedicated configuration file or by using the env command.

Finally, another required parameter that is important to set is the API Keys that is used by the application.  Without it, the app will not start up.  This file is stored in a json file located in "/material-flask/apps/apihandler/api.config.json".  An example of how this file looks like is:

```json
{
    "Bearer Token": "",
    "Bearer Token July 2023": "",
    "Bearer Token August 2023": "",
    "Bearer Token September 2023": "",
    "Bearer Token October 2023": ""
}
```

**Note:** Should you be using GNU Guix, make sure that you are using the latest channels file provided in our CI [here](https://ci.genenetwork.org/channels.scm).  We recommend you use [guix profiles](https://issues.genenetwork.org/topics/guix-profiles).

### Configuration Variables


| Variable    | Used By/For       | Description                                     |
|-------------|-------------------|-------------------------------------------------|
| ASSETS_ROOT | Flask             | Root of where the static files are located      |
| SECRET_KEY  | Flask             | Used by flask to securely sign session cookies |
| SQLITE_URI  | SQLite connection | Used to configure connections with sqlite      |


## Installation

The recommended way to install and run this application is by using [GNU Guix](https://guix.gnu.org/).

The first step is to [install](https://guix.gnu.org/manual/en/html_node/System-Installation.html) [GNU Guix](https://guix.gnu.org/) as your system.  If you are already using some other Linux distribution, [install](https://guix.gnu.org/manual/en/html_node/Installation.html) GNU Guix as a package manager on your system.

Once you have GNU Guix installed on your computer, you can now start **material-flask** in one of three ways:

- Using a development shell/environment
- Using a guix profile

Another documented way, albeit not recommended, is using docker.

One you start the app, the site should be up at localhost:5005.

### Guix Shell

This is the recommended way to start **material-flask** if you intend to do any development on **GN-LLMs**.  To do this, you need to be inside the **material-flask** folder inside the **GN-LLMS** repository:

```sh
cd material-flask/

env ASSETS_ROOT="/static/assets" \
	SECRET_KEY="our-little-secret" \
	SQLITE_URI="sqlite:///gnqa-db.sqlite3" \
	guix shell bash coreutils which vim \
     --share=$PWD --container --network \
	 --development --file=../guix.scm -- \
	 env SCRIPT_NAME=/ai gunicorn \
	 --config $PWD/gunicorn-cfg.py run:app
```

The `--network` option allows the container to share the host network, and you can access the application with: "http://localhost:<port>".

The `--development` option installs all the dependencies in the shell that you need for development - including those which won't be in production but are needed for dev-work.

The `--share` and `--expose` options are used to expose specific directories on the host system to your container.  The `--expose` option exposes the specified directory in **read-only** mode.  You cannot write to such a share.  The `--share` option allows the shared directory to be writable from the shell.

The `--share` and `--expose` options can be repeated expose as many directories to the shell as are needed.

The `--container` option creates a container environment completely isolated from the rest of your system.  This is the recommended way to do your development.  Without the option, your host environment bleeds into your shell.

Since providing the `--container` option isolates your shell, it means you will not have access to some command in the host within the shell environment.  A lot of the times, this is a non-issue, and you can get by without them.  If, however, you find yourself in one of the vanishingly-small instances where you require to leak your host environment into your development environment, then you know to simply omit the option.

### Guix Profile

You can install **genenetwork-qa** package into a profile with:

```sh
guix package --install-from-file=guix.scm \
	--profile="${HOME}/.guix-extra-profiles/gn-genenetwork-qa"
```

You can then source that profile to run the application:

```sh
source ~/.guix-extra-profiles/gn-genenetwork-qa/etc/profile

cd material-flask

env ASSETS_ROOT="/static/assets" \
	SECRET_KEY="our-little-secret" \
	SQLITE_URI="sqlite:///gnqa-db.sqlite3" \
	SCRIPT_NAME=/ai gunicorn \
	--config gunicorn-cfg.py run:app
```

### Using Docker

The nginx configuration file needs to be modified for the docker container to work correctly.

```sh
cd material-flask/nginx
mv matflask-app.old matflask-app.conf
cd ../..
docker build . -t matflask_app
docker-compose up
```

The site should be up at localhost:5095.
