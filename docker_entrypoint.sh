#!/bin/sh
set -ex

# Move to application directory
cd /app

# Run any new database migrations
python manage.py makemigrations App
python manage.py migrate

# Load sample data if database is empty
if [ ! -f /app/storage/db.sqlite3 ]; then
  echo "Loading fixtures..."
  python manage.py setup_groups
  python manage.py loaddata App/fixtures/collections.json
  python manage.py loaddata App/fixtures/users.json
  python manage.py loaddata App/fixtures/machineries.json
  python manage.py loaddata App/fixtures/machineryfaults.json
else
  echo "DB already exists, skipping setup."
fi

# Run Django’s development server
python manage.py runserver 0.0.0.0:8000
