from django.core.wsgi import get_wsgi_application
import os
import sys

# Add the project directory to the sys.path
sys.path.append('/var/www/ecommerce_test')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
