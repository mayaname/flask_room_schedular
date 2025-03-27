# Flask Room Scheduler w/ FullCalendar

## Description

This is a Flask conference/training room scheduling application. The app uses Flask-Admin, Flask-Migrate, SQLAlchemy, and SQLite3 for database management. Other major modules include Flask-Login for user authentication and Flask-WTF for form processing. The free version of FulCalendar from FulCalendar.io displays reservations in a calendar view. Reservations are also presented in a tabular format. With the exception of the calendar and Admin Panel, all scripting and styling files are local.

## Features

- All future reservation are displayed on the Home page without a login requirement
- Schedulers must login and can only reserve rooms in their department
- Schedulers can only update and delete their own reservations
- On login, the schedulers are redirect to a page showing future reservations in their department
- Also on login, links to the reservation's details are displayed 
- The departmental reservation page provides the option to add a new reservation.
- The start time for a new reservation must be after the current date and time.
- The reservation for a specific room cannot overlap an existing one for that room
- The reservation's details page displays information about the reservation
- The details pages show the scheduler's contact info (Note the option to email is not implemented)
- The scheduler's contact info is also displayed as a modal in the reservation tables
- The FulCalendar view displays the room name and start time for the reservations
- Each reservation on the calendar has a tooltip showing the start and end times
- The Admin Panel is restricted to a user with admin privileges 
- The Admin can create, update, and delete users and rooms.

### Notes
- Code to use SendMail for email handling is available on my GitHub <a class="text_link" href="#" target="_blank">Flask Journal</a> site.
- The paid version of FulCalendar allows for significantly more options


