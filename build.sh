#!/usr/bin/env bash
# Railway/Render build script
set -o errexit

pip install -r requirements.txt

mkdir -p staticfiles
python manage.py collectstatic --no-input
