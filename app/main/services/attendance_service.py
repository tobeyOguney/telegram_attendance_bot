import datetime

from app.main import db
from app.main.models.attendance import Attendance
from app.main.models.user import User


def create_attendance(data):
    new_attendance = Attendance(
        purpose = data['purpose'],
        alias = data['alias'],
        group_id = data['group_id'],
        min_duration = data['min_duration'],
        is_open = True,
        timestamp = datetime.datetime.utcnow()
    )
    save_changes(new_attendance)
    return new_attendance, 201


def get_attendance(group_id, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        return attendance, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.'
        }
        return response_object, 409


def get_checkedin_users(group_id, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        return attendance.checkedin_users, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.'
        }
        return response_object, 409


def get_checkedout_users(group_id, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        return attendance.checkedout_users, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Attendance does not exist.'
        }
        return response_object, 409


def close_attendance(group_id, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        attendance.is_open = False
        attendance.alias = "closed"
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


def checkin_attendance(group_id, alias, data):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance and attendance.is_open:
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if user:
            attendance.checkedin_users.append(user)
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


def checkout_attendance(group_id, alias, data):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance and attendance.is_open:
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if user:
            if (datetime.datetime.utcnow() - attendance.timestamp).seconds >= attendance.min_duration*60:
                attendance.checkedout_users.append(user)
                save_changes(attendance)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully commited.'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Too early to check out.',
                }
                return response_object, 409
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


def remove_attendance(group_id, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        Attendance.query.filter_by(group_id=group_id, alias=alias).delete()
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

