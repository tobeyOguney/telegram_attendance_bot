
from flask import request
from flask_restplus import Resource

from ..utils.dto import UserDto
from ..services.user_service import (create_user, get_user,
    update_user, remove_user, get_all_users)
api = UserDto.api
_user = UserDto.user
_user_update = UserDto.user_update


@api.route('/')
class User(Resource):
    @api.doc('List Of Registered Users')
    @api.marshal_list_with(_user)
    def get(self):
        """List all registered users"""
        return get_all_users()
    
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return create_user(data=data)


@api.route('/<telegram_id>')
@api.param('telegram_id', "The User's Telegram ID")
@api.response(404, 'User not found.')
class UserProfile(Resource):
    @api.doc('get a user\'s profile')
    @api.marshal_with(_user)
    def get(self, telegram_id):
        """get a user\'s profile given its identifier"""
        user = get_user(telegram_id)
        return user

    @api.doc('updates an existing user')
    @api.expect(_user_update, validate=True)
    @api.marshal_with(_user)
    def put(self, telegram_id):
        """Updates an existing User """
        data = request.json
        return update_user(telegram_id, data=data)

    @api.doc('remove a user\'s profile')
    def delete(self, telegram_id):
        """removes a user's profile"""
        return remove_user(telegram_id)
    