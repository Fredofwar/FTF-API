from decouple import config
import os

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    MONGO_URL = os.environ.get('MONGO_URL')
    if not MONGO_URL:
        MONGO_URL = "mongodb://localhost:27017/FTF"
    MONGO_URI = MONGO_URL
    
config = {
    'development': DevelopmentConfig
}