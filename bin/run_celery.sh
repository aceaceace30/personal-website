#!/usr/bin/env bash

cd /home/ace/personal-website || exit
exec celery -A personal_profile worker -l info --pool=solo