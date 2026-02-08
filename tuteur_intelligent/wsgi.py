"""
WSGI config for tuteur_intelligent project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuteur_intelligent.settings')

application = get_wsgi_application()
