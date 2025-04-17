#!/bin/sh

# Exit on error
set -e

# Check if superuser exists, if not, create one
# echo "Creating superuser if not exists..."
# python manage.py shell <<EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username="admin").exists():
#     User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
#     print("Superuser created.")
# else:
#     print("Superuser already exists.")
# EOF

mkdir -p /tmp/django_sessions

# python manage.py import_csv_files

echo "Starting Django server..."
exec "$@"
