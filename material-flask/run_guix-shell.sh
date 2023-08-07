#!/usr/bin/env sh

guix shell bash coreutils which vim --share=$PWD -C --network -f guix.scm -- env SCRIPT_NAME=/ai gunicorn --config $PWD/gunicorn-cfg.py run:app
