# StayEase Hotel Booking System

StayEase is a Python-based hotel booking website built with Flask. Visitors can browse and search hotels, view hotel details, submit demo reservations, and see booking confirmations and booking history.

This project is intended for local learning and demonstration. It does not process payments or provide production booking or account-management services.

## Technology

- **Python 3** for application logic.
- **Flask** for the web server, URL routes, request handling, and page rendering.
- **SQLite** for local hotel and booking data. Python's built-in `sqlite3` module is used; no separate database server is needed.
- **Jinja, HTML, and CSS** for server-rendered pages and styling.
- **JavaScript** for small browser-side interactions, such as keeping the checkout date after the check-in date.

## Features

- Browse hotels ordered by guest rating.
- Search hotels by name or location.
- View hotel descriptions, ratings, prices, and amenities.
- Submit a reservation with guest details, dates, guest count, and room count.
- Calculate a demo booking total from the nightly rate, number of nights, and rooms.
- View a booking confirmation and the saved booking history.

## Project structure

```text
.
├── app.py                  # Flask application and routes
├── database.py             # SQLite setup and data-access functions
├── hotels.db               # Local SQLite database (created/initialized by the app)
├── requirements.txt        # Python package dependencies
├── start_website.bat       # Windows one-click launcher
├── static/
│   ├── css/style.css       # Site styles
│   └── js/main.js          # Browser-side interactions
└── templates/
    ├── base.html           # Shared page layout and navigation
    ├── index.html          # Hotel search and listings
    ├── hotel_details.html  # Hotel details
    ├── booking.html        # Reservation form
    └── my_bookings.html    # Confirmation and booking history
```

## Run on Windows

1. Install Python 3 and ensure `python` is available on your PATH.
2. Double-click `start_website.bat`.
3. The launcher checks for Flask, installs the requirements if necessary, starts the Flask server, and opens the site in your browser at <http://127.0.0.1:5000>.
4. Keep the minimized **StayEase Website** command window open while using the site. Close that window to stop the server.

If the launcher cannot find Python, install Python 3 and enable the option to add it to PATH, then try again.

## Run manually

Open a terminal in the project folder and run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Then visit <http://127.0.0.1:5000>. Press `Ctrl+C` in the terminal to stop the server.

## Workflow

### Visitor booking flow

1. The visitor opens `/`. The `home` route in `app.py` asks `database.py` for the hotel list and renders `index.html`.
2. A search submits a GET request to `/` with a search term. The database looks for matches in hotel names and locations.
3. Selecting a hotel opens `/hotel/<hotel_id>`. Flask loads the hotel record and renders `hotel_details.html`.
4. Selecting **Book this hotel** opens `/book/<hotel_id>`. Flask renders `booking.html` with the hotel's details and today's date.
5. On form submission, Flask validates the guest information, dates, guest count, and room count. It calculates the total as `nightly price × nights × rooms`.
6. `database.py` saves the reservation in SQLite. Flask redirects to `/confirmation/<booking_id>` and displays the confirmation.
7. The visitor can open `/bookings` to see all saved reservations.

### Application startup and data

- Running `app.py` creates the Flask app and calls `initialize_database()`.
- `database.py` creates the `hotels` and `bookings` tables if they do not exist.
- If the hotels table is empty, sample hotel records are inserted.
- SQLite stores the database in `hotels.db` in the project folder. Existing bookings remain there between server restarts.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Hotel listings and optional search |
| `/hotel/<hotel_id>` | Hotel details |
| `/book/<hotel_id>` | Booking form and submission |
| `/confirmation/<booking_id>` | Booking confirmation |
| `/bookings` | Booking history |

## Notes

- Hotel images are loaded from external Unsplash URLs, so those images require an internet connection.
- The current Flask configuration enables debug mode and uses a demo secret key. These settings are for local development only; do not deploy this configuration publicly as-is.
