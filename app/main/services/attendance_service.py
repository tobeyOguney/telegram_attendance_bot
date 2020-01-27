import datetime

from app.main import db
from app.main.models.attendance import Attendance
from app.main.models.user import User


def create_attendance(data):
    new_attendance = Attendance(
        purpose = data['purpose'],
        is_open = True,
        timestamp = datetime.datetime.utcnow()
    )
    save_changes(new_attendance)
    return new_attendance, 201


def get_attendance(timestamp):
    attendance = Attendance.query.filter_by(timestamp=timestamp).first()
    if attendance:
        return attendance, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.'
        }
        return response_object, 409


def get_users(timestamp):
    attendance = Attendance.query.filter_by(timestamp=timestamp).first()
    if attendance:
        return attendance.users, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.'
        }
        return response_object, 409


def close_attendance(timestamp):
    attendance = Attendance.query.filter_by(timestamp=timestamp).first()
    if attendance:
        attendance.is_open = False
        save_changes(attendance)
        response_object = {
            'status': 'success',
            'message': 'Successfully closed.'
        }
        return response_object, 201
    else:
        response_object = {
                'status': 'fail',
                'message': 'Attendance does not exist.',
        }
        return response_object, 409


def commit_attendance(timestamp, data):
    attendance = Attendance.query.filter_by(timestamp=timestamp).first()
    if attendance and attendance.is_open:
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if user:
            attendance.users.append(user)
            save_changes(attendance)
            response_object = {
                'status': 'success',
                'message': 'Successfully commited.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.',
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance is closed or does not exist.',
        }
        return response_object, 409


def remove_attendance(timestamp):
    attendance = Attendance.query.filter_by(timestamp=timestamp).first()
    if attendance:
        Attendance.query.filter_by(timestamp=timestamp).delete()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully removed.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()

