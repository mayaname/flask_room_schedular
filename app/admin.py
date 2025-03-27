'''
Program: Admin_
Author: Maya Name
Creation Date: 03/25/2025
Revision Date: 
Description: Admin classes for Flask Room Scheduler application


'''

from flask import redirect, url_for 
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from .config import Config


# Restrictions for viewing Admin page and model views

class AppAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == Config.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login')) 
            

class RoomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
    
