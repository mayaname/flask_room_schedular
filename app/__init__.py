'''
Program: __init__
Author: Maya Name
Creation Date: 03/05/2025
Revision Date: 
Description: Initialization file for Flask Room Scheduler application



 
'''

from flask import Flask
from .config import Config
from . import errors
from .admin import AppAdminView, RoomModelView, UserModelView
from .auth import auth
from .extensions import admin, db, login_manager, migrate
from .models import User, Room
from .routes import pages


def create_app():
    app = Flask(__name__)

    # Sets config for development
    app.config.from_object(Config)
    # app.config['FLASK_ADMIN_SWATCH'] = 'bootstrap3'  # Before admin.init_app()

    # Initialize extensions
    admin.init_app(app, index_view=AppAdminView())

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Set view to login route 
    login_manager.login_view = 'pages.login'
    login_manager.login_message = 'You are not authorized to modify site content.'
    login_manager.login_message_category = 'warning'

    # Get user by id for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set content for admin
    @app.context_processor
    def inject_admin():
        print(app.config.get('ADMIN'))
        return {'ADMIN': app.config.get('ADMIN')} 
  
    # Define admin views
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoomModelView(Room, db.session))
    
    # Error handlers
    app.register_error_handler(403, errors.forbidden)
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(500, errors.internal_server_error)   

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(pages)

    return app