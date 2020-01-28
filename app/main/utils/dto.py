from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user_id = api.model('user_id', {
        "telegram_id": fields.String(required=True, description="user's ID number")
    })
    user = api.model('user', {
        "telegram_id": fields.String(required=True, description="user's ID number"),
        "first_name": fields.String(required=True, description="user's first name"),
        "last_name": fields.String(required=True, description="user's last name"),
        "is_admin": fields.Boolean(required=True, description="user's admin status"),
        "registration_id": fields.String(required=True, description="user's registration ID")
    })
    user_update = api.model('user_update', {
        "first_name": fields.String(required=True, description="user's first name"),
        "last_name": fields.String(required=True, description="user's last name"),
        "is_admin": fields.Boolean(required=True, description="user's admin status"),
        "registration_id": fields.String(required=True, description="user's registration ID")
    })


class AttendanceDto:
    api = Namespace('attendance', description='attendance related operations')
    attendance = api.model('attendance', {
        "is_open": fields.Boolean(required=True, description="attendance open status"),
        "group_id": fields.String(required=True, description="ID of corresponding Telegram group"),
        "alias": fields.String(required=True, description="alias of the attendance"),
        "min_duration": fields.Integer(required=True, description="minimum duration for checkout")
    })
    attendance_response = api.model('attendance_response', {
        "timestamp": fields.String(required=False, description="attendance timestamp"),
        "is_open": fields.Boolean(required=True, description="attendance open status"),
        "group_id": fields.String(required=True, description="ID of corresponding Telegram group"),
        "alias": fields.String(required=True, description="alias of the attendance"),
        "min_duration": fields.Integer(required=True, description="minimum duration for checkout")
    })