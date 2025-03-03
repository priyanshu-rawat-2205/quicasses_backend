import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

DB_USERNAME = os.getenv('DB_USERNAME', 'priyanshu-local')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'quicasses')



UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'json', 'csv', 'pdf', 'png', 'jpg'}

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    JWT_ALGORITHM = "HS256" 
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDUS_DB = 0
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

