import logging
import os
import sys
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Define base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env file explicitly
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# Ensure project directory is in system path
sys.path.append(BASE_DIR)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# Explicitly log environment variables to verify
logger = logging.getLogger(__name__)
logger.info("SENDER_EMAIL: %s", os.getenv("SENDER_EMAIL"))
logger.info("SENDER_PASSWORD: %s", os.getenv("SENDER_PASSWORD"))

# Get WSGI application
application = get_wsgi_application()
