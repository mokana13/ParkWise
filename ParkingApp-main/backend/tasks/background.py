# backend/tasks/background.py
"""
Celery tasks for booking/release emails, daily reminders,
monthly reports, and CSV export, using explicit Flask app imports.
"""

from datetime import datetime, timedelta
from io import StringIO
import csv

from flask_mail import Message
from flask import render_template_string

from backend.extensions import celery, mail
from backend.models import User, Reservation


@celery.task(name='tasks.send_booking_email')
def send_booking_email(to_email, body):
    """
    Send booking confirmation email to the user.
    """
    from backend.app import app  # ✅ Import locally to avoid circular import

    with app.app_context():
        msg = Message(
            subject="Booking Confirmed",
            recipients=[to_email],
            body=body
        )
        mail.send(msg)


@celery.task(name='tasks.send_release_email')
def send_release_email(to_email, body):
    """
    Send parking spot release email to the user.
    """
    from backend.app import app  # ✅ Import locally to avoid circular import

    with app.app_context():
        msg = Message(
            subject="Parking Spot Released",
            recipients=[to_email],
            body=body
        )
        mail.send(msg)


@celery.task(name='tasks.send_daily_reminders')
def send_daily_reminders():
    """
    Email users who never booked or haven’t booked in the last 3+ days.
    """
    from backend.app import app  # ✅ Import locally

    cutoff = datetime.utcnow() - timedelta(days=3)
    with app.app_context():
        users = User.query.filter_by(role='user').all()
        for u in users:
            last = (
                Reservation.query
                .filter_by(user_id=u.id)
                .order_by(Reservation.start_time.desc())
                .first()
            )
            if not last or last.start_time < cutoff:
                body = (
                    f"Hi {u.fullname},\n\n"
                    "We noticed you haven't parked with us recently. "
                    "Book a spot today!\n\n– ParkWise Team"
                )
                msg = Message(
                    subject="We miss you at ParkWise",
                    recipients=[u.email],
                    body=body
                )
                mail.send(msg)


@celery.task(name='tasks.generate_monthly_reports')
def generate_monthly_reports():
    """
    Generate monthly summary report and email it to all users.
    """
    from backend.app import app  # ✅ Import locally

    with app.app_context():
        now = datetime.utcnow()
        first_day = datetime(now.year, now.month, 1)
        last_day = datetime(now.year, now.month + 1, 1) if now.month < 12 else datetime(now.year + 1, 1, 1)

        users = User.query.all()
        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.end_time >= first_day,
                Reservation.end_time < last_day
            ).all()

            total_spent = sum(r.cost for r in reservations if r.cost)
            total_visits = len(reservations)

            lot_counts = {}
            for res in reservations:
                if res.parking_spot and res.parking_spot.lot:
                    lot_name = res.parking_spot.lot.name
                    lot_counts[lot_name] = lot_counts.get(lot_name, 0) + 1

            favorite_lot = max(lot_counts.items(), key=lambda x: x[1])[0] if lot_counts else "N/A"

            msg = Message(
                subject="ParkWise Monthly Report",
                sender="noreply@parkwise.com",
                recipients=[user.email]
            )
            msg.body = f"""ParkWise Monthly Report
User: {user.fullname}

Total Visits: {total_visits}
Total Spent: ₹{total_spent}
Favorite Lot: {favorite_lot}
"""
            mail.send(msg)


@celery.task(name='tasks.export_reservations_to_csv')
def export_reservations_to_csv(user_id):
    """
    Generate CSV of all reservations for a user and send it via email.
    """
    from backend.app import app  # ✅ Import locally

    with app.app_context():
        u = User.query.get(user_id)
        resvs = Reservation.query.filter_by(user_id=user_id).all()

        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(['Reservation ID', 'Lot', 'Spot', 'Start', 'End', 'Cost'])
        for r in resvs:
            writer.writerow([
                r.id,
                r.lot.name,
                r.spot.spot_number,
                r.start_time.isoformat(),
                r.end_time.isoformat() if r.end_time else '',
                getattr(r, 'cost', '')
            ])

        msg = Message(
            subject="Your ParkWise Reservation History",
            recipients=[u.email],
            body="Find your reservation history attached."
        )
        msg.attach("reservations.csv", "text/csv", buf.getvalue())
        mail.send(msg)
