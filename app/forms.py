"""
Program: Forms
Author: Maya Name
Creation Date: 03/11/2025
Revision Date: 
Description: Forms file for Flask Room Scheduler application

Revisions:


"""

import sqlalchemy as sa
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms_alchemy import QuerySelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import Email, EqualTo, InputRequired, ValidationError
from app.extensions import db
from app.models import User, Room

# Query function for the QuerySelectField
def room_choices():
    if current_user.is_authenticated:
        return Room.query.filter(Room.department == current_user.department).all()
    return []


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign In')


class SigninForm(FlaskForm):
    firstname = StringField('First name', validators=[InputRequired()])
    lastname = StringField('Last name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class ReservationForm(FlaskForm):
    start_time = DateTimeLocalField("Start Time: ", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    end_time = DateTimeLocalField("End Time: ", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    room_id = QuerySelectField(
        "Room",
        query_factory=room_choices,
        get_label="room_name",
        allow_blank=False,
        validators=[InputRequired()]
    )
    submit = SubmitField('Reserve')

    def validate_end_time(self, field):
        if self.start_time.data and field.data <= self.start_time.data:
            raise ValidationError("End time must be after start time.")
        

class UpdateReservationForm(FlaskForm):
    start_time = DateTimeLocalField("Start Time: ", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    end_time = DateTimeLocalField("End Time: ", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    room_id = QuerySelectField(
        "Room",
        query_factory=room_choices,
        get_label="room_name",
        allow_blank=False,
        validators=[InputRequired()]
    )
    submit = SubmitField('Update')
