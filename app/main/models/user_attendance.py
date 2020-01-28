from .. import db

class CheckedInUserAttendance(db.Model):
    __tablename__ = 'checkedin_user_attendance'
    user_id = db.Column(db.String, db.ForeignKey('user.telegram_id'),  primary_key=True)
    attendance_id = db.Column(db.String, db.ForeignKey('attendance.timestamp'), primary_key=True)


class CheckedOutUserAttendance(db.Model):
    __tablename__ = 'checkedout_user_attendance'
    user_id = db.Column(db.String, db.ForeignKey('user.telegram_id'),  primary_key=True)
    attendance_id = db.Column(db.String, db.ForeignKey('attendance.timestamp'), primary_key=True)