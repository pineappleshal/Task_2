import os

BASE_URL = os.getenv('STELLAR_BASE_URL', 'https://qa-stellarburgers.education-services.ru').rstrip('/')
TIMEOUT = (5, 30)
