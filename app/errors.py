"""
Program: Errors
Author: Maya Name
Creation Date: 01/13/2025
Revision Date:
Description: Display error pages

Revisions: 

"""

from flask import render_template
from app.extensions import db

# Ref to images on OneDrive
# IMAGE_REF = 'https://1drv.ms/i/c/577c91344c497a71/'

ERROR = {
    '403_IMG':'error.webp',
    '403_HEADING':'Access Forbidden',
    '403_MESSAGE_1':'It appears that you do not have authorization',
    '403_MESSAGE_2':'to view the requested material.',
    '403_MESSAGE_3':'Slip the admin a twenty, and try again!',

    '404_IMG':'404_error.jpg',
    '404_HEADING':'Page Not Found',
    '404_MESSAGE_1':'Oh no, I am so embarrassed!',
    '404_MESSAGE_2':'I cannot seem to find the page you requested.',
    '404_MESSAGE_3':'Click the Home link above to go back.',

    '500_IMG':'500_error.webp',
    '500_HEADING':'Internal Server Error',
    '500_MESSAGE_1':'Damn, not again!',
    '500_MESSAGE_2':'I\'ll get around to fixing this steaming pile shortly.',
    '500_MESSAGE_3':'Try refreshing the page, or come back later.'
}

def forbidden(e):
    error_type = '403'
    return render_template("error.html", 
                        #    IMAGE_REF=IMAGE_REF,
                           ERROR_IMG=ERROR['403_IMG'],
                           ERROR_HEADING = ERROR['403_HEADING'],
                           ERROR_MESSAGE_1 = ERROR['403_MESSAGE_1'],
                           ERROR_MESSAGE_2 = ERROR['403_MESSAGE_2'],
                           ERROR_MESSAGE_3 = ERROR['403_MESSAGE_3'],
                           error_type=error_type), 403

def page_not_found(e):
    error_type = '404'
    return render_template("error.html", 
                        #    IMAGE_REF=IMAGE_REF,
                           ERROR_IMG=ERROR['404_IMG'],
                           ERROR_HEADING = ERROR['404_HEADING'],
                           ERROR_MESSAGE_1 = ERROR['404_MESSAGE_1'],
                           ERROR_MESSAGE_2 = ERROR['404_MESSAGE_2'],
                           ERROR_MESSAGE_3 = ERROR['404_MESSAGE_3'],
                           error_type=error_type), 404

def internal_server_error(e):
    error_type = '500'
    db.session.rollback()
    return render_template('error.html', 
                        #    IMAGE_REF=IMAGE_REF,
                           ERROR_IMG=ERROR['500_IMG'],
                           ERROR_HEADING = ERROR['500_HEADING'],
                           ERROR_MESSAGE_1 = ERROR['500_MESSAGE_1'],
                           ERROR_MESSAGE_2 = ERROR['500_MESSAGE_2'],
                           ERROR_MESSAGE_3 = ERROR['500_MESSAGE_3'],
                           error_type=error_type), 500