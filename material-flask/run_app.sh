#!/bin/env sh

gunicorn --config gunicorn_cfg.py run:app
