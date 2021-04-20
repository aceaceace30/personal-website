#!/usr/bin/env bash

cd /home/ace/personal-website || exit
source venv/bin/activate
exec celery -A personal_website worker -l info --pool=solo
