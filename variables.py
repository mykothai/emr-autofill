import os
from dotenv import load_dotenv

load_dotenv()
site = os.environ.get('SITE')
browser = os.environ.get('BROWSER')
env = os.environ.get('ENV')
if env == 'production':
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
else:
    user = os.environ.get('TEST_USER')
    password = os.environ.get('TEST_PASSWORD')
input_delay = 0.5
