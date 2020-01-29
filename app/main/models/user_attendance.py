import datetime

from .. import db


class CheckedInUserAttendance(db.Model):
    __tablename__ = 'checkedin_user_attendance'
    user_id = db.Column(db.String, db.ForeignKey('user.telegram_id'),  primary_key=True)
    attendance_id = db.Column(db.DateTime, db.ForeignKey('attendance.timestamp'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class CheckedOutUserAttendance(db.Model):
    __tablename__ = 'checkedout_user_attendance'
    user_id = db.Column(db.String, db.ForeignKey('user.telegram_id'),  primary_key=True)
    attendance_id = db.Column(db.DateTime, db.ForeignKey('attendance.timestamp'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
