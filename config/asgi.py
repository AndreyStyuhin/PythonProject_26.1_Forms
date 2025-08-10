# config/asgi.py
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
