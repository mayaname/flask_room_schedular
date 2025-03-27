"""
Program: App
Author: Maya Name
Creation Date: 03/05/2025
Revision Date: 
Description: File that launches the Flask Room Scheduler application

Revisions:

"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()