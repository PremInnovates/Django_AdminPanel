"""
WSGI config for ChargeNow project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chargenow.settings')

application = get_wsgi_application()
