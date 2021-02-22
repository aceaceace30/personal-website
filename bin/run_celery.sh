#!/usr/bin/env bash

exec celery -A personal_profile worker -l info --pool=solo