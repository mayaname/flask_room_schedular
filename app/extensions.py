"""
Program: Extensions
Author: Maya Name
Creation Date: 03/08/2025
Revision Date: 
Description: Extensions file for Flask Room Scheduler application

Revisions:


"""

from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


admin = Admin()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()