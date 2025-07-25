from .base import *

import socket

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "0.0.0.0,127.0.0.1,192.168.0.104",
).split(",")

INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(",")

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
