import os
import sys

# Добавляем папку apps в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "products"))

# Указываем правильный модуль настроек
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
