from .. import db
from .user_attendance import UserAttendance

class Attendance(db.Model):
    """
    A model for storing attendance related details
    """
    __tablename__ = "attendance"
    
    timestamp = db.Column(db.DateTime, primary_key=True)
    purpose = db.Column(db.String, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)
    users = db.relationship("User", secondary='user_attendance', backref="attendance")
