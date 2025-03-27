'''
Program: Models
Author: Maya Name
Creation Date: 03/08/2025
Revision Date: 
Description: Data structure models for Flask Room Scheduler application

Revisions:


'''


from datetime import datetime
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db  

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    lastname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), index=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    ext: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5))
    building: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1))
    department: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))

    # Relationship to Reservation
    reservations: so.Mapped[list["Reservation"]] = so.relationship(back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User: {self.username}>'


class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    room_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    building: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1))
    department: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    capacity: so.Mapped[int] = so.mapped_column()
    computer: so.Mapped[bool] = so.mapped_column()
    projector: so.Mapped[bool] = so.mapped_column()
    whiteboard: so.Mapped[bool] = so.mapped_column()

    # Relationship to Reservation
    reservations: so.Mapped[list["Reservation"]] = so.relationship(back_populates="room")

    def __repr__(self):
        return f'<Room: {self.room_name}>'


class Reservation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    start_time: so.Mapped[datetime] = so.mapped_column(index=True)
    end_time: so.Mapped[datetime] = so.mapped_column(index=True)

    # Foreign keys
    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("room.id"), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)

    # Relationships
    room: so.Mapped["Room"] = so.relationship(back_populates="reservations")
    user: so.Mapped["User"] = so.relationship(back_populates="reservations")

    def __repr__(self):
        return f'<Reservation: Room {self.room_id} by User {self.user_id} from {self.start_time} to {self.end_time}>'

    @staticmethod
    def is_room_available(room_id, start_time, end_time):
        """
        Check if the room is available for the given time slot.
        """
        conflicting_reservations = db.session.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).count()
        return conflicting_reservations == 0
