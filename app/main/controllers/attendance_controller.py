
from flask import request
from flask_restplus import Resource

from ..utils.dto import AttendanceDto, UserDto
from ..services.attendance_service import (create_attendance, get_attendance, get_users,
    remove_attendance, commit_attendance, close_attendance)
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
    @api.marshal_with(_attendance_response)
    def post(self):
        """Creates a new Attendance """
        data = request.json
        return create_attendance(data=data)


@api.route('/user/<timestamp>')
@api.param('timestamp', 'The Attendance timestamp')
class StudentAttendance(Resource):
    @api.doc('List Of Commited Users')
    @api.marshal_list_with(_user)
    def get(self, timestamp):
        """List all commited users"""
        return get_users(timestamp)


@api.route('/profile/<timestamp>')
@api.param('timestamp', 'The Attendance timestamp')
@api.response(404, 'Attendance not found.')
class AttendanceProfile(Resource):
    @api.doc('get a attendance\'s profile')
    @api.marshal_with(_attendance_response)
    def get(self, timestamp):
        """get a attendance\'s profile given its identifier"""
        attendance = get_attendance(timestamp)
        return attendance

    @api.doc('remove a attendance\'s profile')
    def delete(self, timestamp):
        """removes a attendance's profile"""
        return remove_attendance(timestamp)


@api.route('/commit/<timestamp>')
@api.param('timestamp', 'The Attendance timestamp')
@api.response(404, 'Attendance not found.')
class CommitAttendanceSession(Resource):
    @api.doc('commit to an attendance session')
    @api.expect(_user_id, validate=True)
    def put(self, timestamp):
        """commits to an attendance session"""
        data = request.json
        return commit_attendance(timestamp=timestamp, data=data)


@api.route('/close/<timestamp>')
@api.param('timestamp', 'The Attendance timestamp')
@api.response(404, 'Attendance not found.')
class CloseAttendanceSession(Resource):
    @api.doc('close an attendance session')
    def put(self, timestamp):
        """closes an attendance session"""
        return close_attendance(timestamp)

