#!/usr/bin/env sh

guix shell bash coreutils zsh which vim --expose=$PWD -C --network -f guix.scm -- gunicorn --config $PWD/gunicorn-cfg.py run:app
