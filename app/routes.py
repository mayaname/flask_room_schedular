'''
Program: Routes_
Author: Maya Name
Creation Date: 02/05/2024
Revision Date: 
Description: Routing for Flask Room Scheduler application


'''


from datetime import datetime, timezone
from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from urllib.parse import urlparse, urljoin
from app.extensions import  db
from app.forms import ReservationForm, UpdateReservationForm
from app.models import Reservation, Room
                       


pages = Blueprint('pages', __name__)

def is_safe_redirect_url(target):
    # Check if the url is safe for redirects 
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
        redirect_url.scheme in ('http', 'https') and
        host_url.netloc == redirect_url.netloc
    )

# Application routes

@pages.route('/', methods=['GET', 'POST'])
@pages.route('/index/', methods=['GET', 'POST'])
def index():
    head_title = 'Home'
    page_title = 'All Future Room Reservations'
    current_time = datetime.now(timezone.utc)  
    page = request.args.get('page', 1, type=int)

    reservations = db.paginate(
        db.select(Reservation)
        .join(Reservation.room)
        .join(Reservation.user)
        .filter(Reservation.start_time > current_time) 
        .order_by(desc(Reservation.start_time)),
        page=page,
        per_page=3,
        error_out=False
    )

    return render_template('index.html',
                           head_title=head_title,
                           page_title=page_title,
                           reservations=reservations.items, 
                           pagination=reservations,
                           )

@pages.route('/all_resv/', methods=['GET', 'POST'])
@login_required
def all_resv():
    head_title = 'All View'
    page_title = 'All Room Reservations'
    page = request.args.get('page', 1, type=int)

    reservations = db.paginate(
        db.select(Reservation)
        .join(Reservation.room)
        .join(Reservation.user)
        .order_by(desc(Reservation.start_time)),
        page=page,
        per_page=3,
        error_out=False
    )

    return render_template('all_resv.html',
                           head_title=head_title,
                           page_title=page_title,
                           reservations=reservations.items, 
                           pagination=reservations,
                           )

@pages.route('/calendar/', methods=['GET', 'POST'])
@login_required
def calendar():
    head_title = 'Calendar View'
    page_title = 'Room Schedule Calendar'
    current_time = datetime.now(timezone.utc) 
    events = []

    reservations = db.session.query(Reservation).join(Reservation.room).filter(Reservation.start_time > current_time).all()

    for reservation in reservations:
        events.append({
            "title": reservation.room.room_name,
            "start": reservation.start_time.isoformat(), 
            "end": reservation.end_time.isoformat()
        })

    return render_template('calendar_resv.html',
                           head_title=head_title,
                           page_title=page_title,
                           events=events
                           )

@pages.route("/add_resv/", methods=["GET", "POST"])
@login_required
def add_resv():
    head_title = 'Reserve Room'
    page_title = 'Reserve a Conference Room'
    form = ReservationForm()

    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        room = form.room_id.data  

        if not Reservation.is_room_available(room.id, start_time, end_time):
            flash("This room is already booked for the selected time.", "error")
            return redirect(url_for("pages.add_resv"))

        new_reservation = Reservation(
            start_time=start_time,
            end_time=end_time,
            room_id=room.id,  
            user_id=current_user.id
        )

        db.session.add(new_reservation)
        db.session.commit()
        flash(f"{room.room_name} reservation successfully added!", "success")

        return redirect(url_for("pages.index"))  

    return render_template("add_resv.html", 
                           head_title=head_title,
                           page_title=page_title,
                           form=form)

@pages.route('/dept_resv/', methods=['GET', 'POST'])
@login_required  
def dept_resv():
    head_title = 'Department View'
    page_title = 'Future Room Reservations'
    page = request.args.get('page', 1, type=int)
    current_time = datetime.now(timezone.utc)  
    user_department = current_user.department  
    page_subtitle = user_department

    reservations = db.paginate(
        db.select(Reservation)
        .join(Reservation.room)
        .join(Reservation.user)
        .filter(
            Reservation.start_time > current_time,  
            Room.department == user_department  
        )
        .order_by(desc(Reservation.start_time)),
        page=page,
        per_page=3,
        error_out=False
    )

    return render_template(
        'dept_resv.html',
        head_title=head_title,
        page_title=page_title,
        page_subtitle=page_subtitle,
        reservations=reservations.items, 
        pagination=reservations,
    )

@pages.route('/details_resv/<int:resv_id>', methods=['GET', 'POST'])
@login_required  
def details_resv(resv_id: int):
    head_title = 'Reservation Details'
    page_title = 'Reservation Details'
    # For delete confirmation modal
    confirm_title = 'Delete Site Confirmation'
    confirm_message = 'Are you sure you want to delete this site?'

    reservation = Reservation.query.options(
        joinedload(Reservation.room), 
        joinedload(Reservation.user)
    ).get_or_404(resv_id)    

    return render_template(
        'details_resv.html',
        head_title=head_title,
        page_title=page_title,
        confirm_title=confirm_title,
        confirm_message=confirm_message,
        reservation=reservation
    )

@pages.route('/update_resv/<int:resv_id>', methods=['GET', 'POST'])
@login_required  
def update_resv(resv_id: int):
    head_title = 'Update Reservation'
    page_title = 'Update Reservation'

    reservation = Reservation.query.get_or_404(resv_id)

    if reservation.user_id == current_user.id:

        form = UpdateReservationForm(obj=reservation)
        form.room_id.data = reservation.room  

        if form.validate_on_submit():
            try:
                new_start_time = form.start_time.data
                new_end_time = form.end_time.data
                new_room_id = form.room_id.data.id  

                if not Reservation.is_room_available(new_room_id, new_start_time, new_end_time):
                    flash("This room is already booked for the selected time.", "error")
                    return redirect(url_for("pages.update_resv", resv_id=resv_id))

                reservation.start_time = new_start_time
                reservation.end_time = new_end_time
                reservation.room_id = new_room_id  

                db.session.commit()
                flash(f'{reservation.room.room_name} reservation updated successfully!', 'success')

                next_page = request.form.get('next') or request.args.get('next')
                if next_page and is_safe_redirect_url(next_page):
                    return redirect(next_page)

                return redirect(url_for('pages.index'))

            except Exception as e:
                db.session.rollback()
                flash(f'Error updating reservation: {str(e)}', 'error')
                return redirect(url_for('pages.index'))
    else:
        flash('You cannot update someone else\'s reservation.', 'error')
        return redirect(url_for('pages.index'))
    
    return render_template(
        'update_resv.html',
        head_title=head_title,
        page_title=page_title,
        form=form,
        reservation=reservation
    )

@pages.get("/delete_resv/<int:resv_id>")
@login_required
def delete_resv(resv_id:int):
    try:
        reservation = db.session.query(Reservation).filter_by(id=resv_id).first()

        if reservation.user_id == current_user.id: 
                
            if reservation:
                db.session.delete(reservation)
                db.session.commit()
                flash(f"Reservation for {reservation.room.room_name} deleted.", category="success")
            else:
                flash("Reservation not found.", category="error")
        else:
            flash('You cannot delete someone else\'s reservation.', 'error')
            return redirect(url_for('pages.index'))           
    except Exception as e:
        flash(f"An error occurred: {str(e)}", category="error")
    finally:
        db.session.close()

    return redirect(url_for("pages.index"))

