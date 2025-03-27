'''
Program: Config
Author: Maya Name
Creation Date: 03/05/2025
Revision Date: 
Description: Configuration for Flask Room Scheduler application


'''

import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') 
    ADMIN = os.environ.get('ADMIN') 