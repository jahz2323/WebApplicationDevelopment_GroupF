#!/bin/sh

set -ex

# Move to application directory
cd /app

# Run any new database migrations
python manage.py makemigrations App
python manage.py migrate

# Load sample data if database is empty
! -f /app/storage/db.sqlite3
  echo "Loading fixtures..."
  python manage.py setup_groups
  python manage.py loaddata App/fixtures/collections.json
  python manage.py loaddata App/fixtures/users.json
  python manage.py loaddata App/fixtures/machineries.json
  python manage.py loaddata App/fixtures/machineryfaults.json

  echo "DB already exists, skipping setup."


# Run Django’s development server
python manage.py runserver 0.0.0.0:8000
