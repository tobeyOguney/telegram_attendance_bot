import datetime

from app.main import db
from app.main.models.user_attendance import CheckedInUserAttendance, CheckedOutUserAttendance
from app.main.models.attendance import Attendance
from app.main.models.user import User


def create_attendance(data):
    user = User.query.filter_by(telegram_id=data['user_id']).first()
    if user.is_admin:
        new_attendance = Attendance(
            alias = data['alias'],
            group_id = data['group_id'],
            min_duration = data['min_duration'],
            is_open = True,
            timestamp = datetime.datetime.utcnow()
        )
        save_changes(new_attendance)
        response_object = {
            'status': 'success',
            'message': 'You have successfully created an attendance session with alias: "{alias}" in the "{group_name}" group.'.format(**data),
            'alias': new_attendance.alias,
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, you need the admin priviledge to create an attendance session.'
        }
        return response_object, 409


def get_attendance(group_id, group_name, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        return attendance, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
        }
        return response_object, 409


def get_checkedin_users(group_id, group_name, alias, user_id):
    user = User.query.filter_by(telegram_id=user_id).first()
    if user.is_admin:
        attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
        if attendance:
            return attendance.checkedin_users, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, you need the admin priviledge to get checked in users.'
        }
        return response_object, 409


def get_checkedout_users(group_id, group_name, alias, user_id):
    user = User.query.filter_by(telegram_id=user_id).first()
    if user.is_admin:
        attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
        if attendance:
            return attendance.checkedout_users, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, you need the admin priviledge to get checked out users.'
        }
        return response_object, 409


def close_attendance(group_id, group_name, alias, user_id):
    user = User.query.filter_by(telegram_id=user_id).first()
    if user.is_admin:
        attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
        if attendance:
            attendance.is_open = False
            save_changes(attendance)
            response_object = {
                'status': 'success',
                'message': 'You have successfully closed "{}" attendance session in the "{}" group.'.format(attendance.alias, group_name)
            }
            return response_object, 201
        else:
            response_object = {
                    'status': 'fail',
                    'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, you need the admin priviledge to close an attendance session.'
        }
        return response_object, 409


def checkin_attendance(group_id, group_name, alias, data):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance and attendance.is_open:
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if user:
            attendance.checkedin_users.append(user)
            save_changes(attendance)
            response_object = {
                'status': 'success',
                'message': 'You have successfully checked into the "{}" attendance session in the "{}" group.'.format(attendance.alias, group_name)
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, you need to register with Mento before you get to check in. Type "mento help" for further information',
            }
            return response_object, 409
    else:
        if not attendance:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
            }
            return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, the "{}" attendance session in the "{}" group has been closed.'.format(alias, group_name)
            }
            return response_object, 409


def checkout_attendance(group_id, group_name, alias, data):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance and attendance.is_open:
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        user_attendance = CheckedInUserAttendance.query.filter_by(user_id=data['telegram_id']).first()
        if not user_attendance:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, you need to check into the "{}" attendance session in the "{}" group to do this.'.format(attendance.alias, group_name),
            }
            return response_object, 409
        if user:
            time_spent = (datetime.datetime.utcnow() - user_attendance.timestamp).seconds
            if time_spent >= attendance.min_duration*60:
                attendance.checkedout_users.append(user)
                save_changes(attendance)
                response_object = {
                    'status': 'success',
                    'message': 'You have successfully checked out of the "{}" attendance session in the "{}" group.'.format(attendance.alias, group_name)
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry, you still have {} minutes left to check out of the "{}" attendance session on the "{}" group.'.format(attendance.min_duration - time_spent//60, attendance.alias, group_name),
                }
                return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, you need to register with Mento before you get to check out. Type "mento help" for further information',
            }
            return response_object, 409
    else:
        if not attendance:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
            }
            return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, the "{}" attendance session in the "{}" group has been closed.'.format(alias, group_name)
            }
            return response_object, 409


def remove_attendance(group_id, group_name, alias):
    attendance = Attendance.query.filter_by(group_id=group_id, alias=alias).first()
    if attendance:
        Attendance.query.filter_by(group_id=group_id, alias=alias).delete()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'You have successfully removed the attendance with alias: "{}" in the "{}" group.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sorry, there is no recorded attendance with alias: "{}" in the "{}" group. Please check the spelling and try again.'.format(alias, group_name)
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()

