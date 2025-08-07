# run_django.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")  # замените на путь к settings.py, если отличается
django.setup()

from django.core.management import call_command
call_command('makemigrations', 'products')
call_command('migrate')
