#!/bin/env sh

export ASSETS_ROOT="$HOME/GN-LLMs/material-flask/apps/static/assets/nos"

guix shell bash coreutils zsh which vim --expose=$PWD -C --network -f guix.scm -- gunicorn --config $PWD/gunicorn-cfg.py run:app
