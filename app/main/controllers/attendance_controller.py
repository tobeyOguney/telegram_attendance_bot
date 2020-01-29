import flask_excel

from flask import request
from flask_restplus import Resource

from ..utils.dto import AttendanceDto, UserDto
from ..services.attendance_service import (create_attendance, get_attendance, get_checkedin_users,
    get_checkedout_users, remove_attendance, checkin_attendance, checkout_attendance, close_attendance)
api = AttendanceDto.api
_attendance = AttendanceDto.attendance
_attendance_response = AttendanceDto.attendance_response
_user = UserDto.user
_user_id = UserDto.user_id


@api.route('/')
class Attendance(Resource):
    @api.expect(_attendance, validate=True)
    @api.response(201, 'Attendance successfully created.')
    @api.doc('create a new attendance')
    def post(self):
        """Creates a new Attendance """
        data = request.json
        return create_attendance(data=data)


@api.route('/checkedin_users/<group_id>/<group_name>/<alias>/<user_id>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.param('user_id', 'The Telegram ID of the requesting user')
class CheckedInAttendance(Resource):
    @api.doc('List Of Checked In Users')
    @api.marshal_list_with(_user)
    def get(self, group_id, group_name, alias, user_id):
        """List all checked in users"""
        return get_checkedin_users(group_id, group_name, alias, user_id)


@api.route('/download/<group_id>/<group_name>/<alias>/<user_id>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.param('user_id', 'The Telegram ID of the requesting user')
class DownloadAttendance(Resource):
    @api.doc('Download User Attendance')
    def get(self, group_id, group_name, alias, user_id):
        """Download user attendance"""
        column_names = ['registration_id', 'first_name', 'last_name']
        response = get_checkedout_users(group_id, group_name, alias, user_id)
        if response[1] == 201:
            return flask_excel.make_response_from_query_sets(response[0], column_names, "xlsx",
                                                            file_name="{}_attendance.xlsx".format(alias))
        else:
            return response


@api.route('/checkedout_users/<group_id>/<group_name>/<alias>/<user_id>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.param('user_id', 'The Telegram ID of the requesting user')
class CheckedOutAttendance(Resource):
    @api.doc('List Of Checked Out Users')
    @api.marshal_list_with(_user)
    def get(self, group_id, group_name, alias, user_id):
        """List all checked out users"""
        return get_checkedout_users(group_id, group_name, alias, user_id)


@api.route('/profile/<group_id>/<group_name>/<alias>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.response(404, 'Attendance not found.')
class AttendanceProfile(Resource):
    @api.doc('get a attendance\'s profile')
    @api.marshal_with(_attendance_response)
    def get(self, group_id, group_name, alias):
        """get a attendance\'s profile given its identifier"""
        attendance = get_attendance(group_id, group_name, alias)
        return attendance

    @api.doc('remove a attendance\'s profile')
    def delete(self, group_id, group_name, alias):
        """removes a attendance's profile"""
        return remove_attendance(group_id, group_name, alias)


@api.route('/checkin/<group_id>/<group_name>/<alias>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.response(404, 'Attendance not found.')
class CheckinAttendanceSession(Resource):
    @api.doc('check into an attendance session')
    @api.expect(_user_id, validate=True)
    def put(self, group_id, group_name, alias):
        """checks into an attendance session"""
        data = request.json
        return checkin_attendance(group_id, group_name, alias, data)



@api.route('/checkout/<group_id>/<group_name>/<alias>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.response(404, 'Attendance not found.')
class CheckoutAttendanceSession(Resource):
    @api.doc('check out of an attendance session')
    @api.expect(_user_id, validate=True)
    def put(self, group_id, group_name, alias):
        """checks out of an attendance session"""
        data = request.json
        return checkout_attendance(group_id, group_name, alias, data)


@api.route('/close/<group_id>/<group_name>/<alias>/<user_id>')
@api.param('group_id', 'The ID of the Telegram group attendance is taken')
@api.param('group_name', 'The title of the Telegram group attendance is taken')
@api.param('alias', 'The alias of the attendance session')
@api.param('user_id', 'The Telegram ID of the requesting user')
@api.response(404, 'Attendance not found.')
class CloseAttendanceSession(Resource):
    @api.doc('close an attendance session')
    def put(self, group_id, group_name, alias, user_id):
        """closes an attendance session"""
        return close_attendance(group_id, group_name, alias, user_id)

