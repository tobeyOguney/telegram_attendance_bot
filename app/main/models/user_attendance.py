from .. import db

class UserAttendance(db.Model):
    __tablename__ = 'user_attendance'
    user_id = db.Column(db.String, db.ForeignKey('user.telegram_id'),  primary_key=True)
    attendance_id = db.Column(db.String, db.ForeignKey('attendance.timestamp'), primary_key=True)