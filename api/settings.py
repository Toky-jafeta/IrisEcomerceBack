from api.configurations.base import *
from api.configurations.dev import *
import os


settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
DATA_UPLOAD_MAX_MEMORY_SIZE=8*1024*1024
WKHTMLTOPDF_PATH = '{}/package/pdf/bin/wkhtmltopdf'.format(PROJECT_ROOT)