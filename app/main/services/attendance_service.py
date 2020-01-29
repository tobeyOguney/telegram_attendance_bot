import datetime

from app.main import db
from app.main.models.user_attendance import CheckedInUserAttendance, CheckedOutUserAttendance
from app.main.models.attendance import Attendance
from app.main.models.user import User


def create_attendance(data):
    new_attendance = Attendance(
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
        user_attendance = CheckedInUserAttendance.query.filter_by(user_id=data['telegram_id']).first()
        if not user_attendance:
            response_object = {
                'status': 'fail',
                'message': 'You have not checked in.',
            }
            return response_object, 409
        if user:
            time_spent = (datetime.datetime.utcnow() - user_attendance.timestamp).seconds
            if time_spent >= attendance.min_duration*60:
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
                    'message': 'You have {} minutes left to check out.'.format(attendance.min_duration - time_spent//60),
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


def collate_attendance(group_id, alias):
    users = [[user.registration_id, user.first_name, user.last_name] for user in get_checkedout_users(group_id, alias)]
    users = [['REGISTRATION_ID', 'FIRST NAME', 'LAST NAME']].extend(users)
    return excel.make_response_from_array(users, 'xlsx')

def save_changes(data):
    db.session.add(data)
    db.session.commit()

