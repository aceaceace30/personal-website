#!/usr/bin/env bash

exec celery -A personal_website worker -l info --pool=solo
