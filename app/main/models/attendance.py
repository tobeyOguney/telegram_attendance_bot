from .. import db
from .user_attendance import CheckedInUserAttendance, CheckedOutUserAttendance

class Attendance(db.Model):
    """
    A model for storing attendance related details
    """
    __tablename__ = "attendance"
    
    timestamp = db.Column(db.DateTime, primary_key=True)
    purpose = db.Column(db.String, nullable=False)
    alias = db.Column(db.String, nullable=False)
    group_id = db.Column(db.String, nullable=False)
    min_duration = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)
    checkedin_users = db.relationship("User", secondary='checkedin_user_attendance', back_populates="checkedin_attendance_sessions")
    checkedout_users = db.relationship("User", secondary='checkedout_user_attendance', back_populates="checkedout_attendance_sessions")
