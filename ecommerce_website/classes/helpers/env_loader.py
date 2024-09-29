import os
from pathlib import Path
from dotenv import load_dotenv


class EnvLoader:

    @staticmethod
    def get_env():
        base_dir = EnvLoader.get_root_path()  # Get the root path if not provided
        load_dotenv(base_dir / '.env')
        return os.getenv('DJANGO_ENV', 'dev')

    @staticmethod
    def get_root_path():
        # Adjust this as necessary for your project structure
        return Path(__file__).resolve().parent.parent.parent
