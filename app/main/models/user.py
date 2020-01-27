from .. import db

class User(db.Model):
    """
    The model for storing details of the users of the Telegram Bot
    """
    __tablename__ = "user"

    telegram_id = db.Column(db.String, primary_key=True)
    registration_id = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    attendance_sessions = db.relationship("Attendance", secondary="user_attendance", backref="user")