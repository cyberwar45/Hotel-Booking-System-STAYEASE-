
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    initialize_database,
    get_hotels,
    get_hotel,
    create_booking,
    get_booking,
    get_all_bookings,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "stayease-exam-demo-change-me"

initialize_database()


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    hotels = get_hotels(search)
    return render_template("index.html", hotels=hotels, search=search)


@app.route("/hotel/<int:hotel_id>")
def hotel_details(hotel_id):
    hotel = get_hotel(hotel_id)
    if not hotel:
        flash("Hotel not found.", "error")
        return redirect(url_for("home"))
    return render_template("hotel_details.html", hotel=hotel)


@app.route("/book/<int:hotel_id>", methods=["GET", "POST"])
def book_hotel(hotel_id):
    hotel = get_hotel(hotel_id)
    if not hotel:
        flash("Hotel not found.", "error")
        return redirect(url_for("home"))

    today = date.today().isoformat()

    if request.method == "POST":
        guest_name = request.form.get("guest_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        check_in = request.form.get("check_in", "")
        check_out = request.form.get("check_out", "")

        try:
            guests = int(request.form.get("guests", "1"))
            rooms = int(request.form.get("rooms", "1"))
            start = date.fromisoformat(check_in)
            end = date.fromisoformat(check_out)
        except (ValueError, TypeError):
            flash("Please enter valid booking details.", "error")
            return render_template("booking.html", hotel=hotel, today=today)

        if not guest_name or not email or not phone:
            flash("Please fill in all personal details.", "error")
        elif "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
        elif len(phone) < 7:
            flash("Please enter a valid phone number.", "error")
        elif start < date.today():
            flash("Check-in cannot be in the past.", "error")
        elif end <= start:
            flash("Check-out must be after check-in.", "error")
        elif not 1 <= guests <= 20 or not 1 <= rooms <= 10:
            flash("Guests or room count is outside the allowed range.", "error")
        else:
            nights = (end - start).days
            total_price = hotel["price"] * nights * rooms

            booking_id = create_booking({
                "guest_name": guest_name,
                "email": email,
                "phone": phone,
                "hotel_id": hotel_id,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "rooms": rooms,
                "total_price": total_price,
            })
            return redirect(url_for("booking_confirmation", booking_id=booking_id))

        return render_template("booking.html", hotel=hotel, today=today)

    return render_template("booking.html", hotel=hotel, today=today)



@app.route("/confirmation/<int:booking_id>")
def booking_confirmation(booking_id):
    booking = get_booking(booking_id)

    if not booking:
        flash("Booking not found.", "error")
        return redirect(url_for("home"))

    return render_template(
        "my_bookings.html",
        booking=booking,
        history_page=False
    )


@app.route("/bookings")
def bookings():
    all_bookings = get_all_bookings()

    return render_template(
        "my_bookings.html",
        bookings=all_bookings,
        history_page=True
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template("base.html", not_found=True), 404


if __name__ == "__main__":
    app.run(debug=True)
