#!/usr/bin/env bash

cd /home/ace/personal-website || exit
source venv/bin/activate
celery -A personal_website beat -l info