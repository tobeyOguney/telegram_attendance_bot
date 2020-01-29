import datetime

from app.main import db
from app.main.models.user import User


def create_user(data):
    user = User.query.filter_by(telegram_id=data['telegram_id']).first()
    if not user:
        new_user = User(
            telegram_id = data['telegram_id'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            registration_id = data['registration_id'],
            is_admin = data['is_admin']
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'You are now registered with Mento.',
            'telegram_id': new_user.telegram_id,
        }
        return response_object, 201
    else:
        if not user.is_admin and data["is_admin"]:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.registration_id = data['registration_id']
            user.is_admin = data['is_admin']
            save_changes(user)
            response_object = {
                'status': 'success',
                'message': 'You now have the admin priviledge.',
                'telegram_id': new_user.telegram_id,
            }
            return response_object, 201
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.registration_id = data['registration_id']
        save_changes(user)
        response_object = {
            'status': 'success',
            'message': 'You have successfully updated your details.',
        }
        return response_object, 201


def get_all_users():
    users = User.query.all()
    if users:
        return users
    else:
        response_object = {
            'status': 'fail',
            'message': 'Users do not exist.',
        }
        return response_object


def get_user(telegram_id):
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if user:
        return user
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 409


def update_user(telegram_id, data):
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if user:
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.registration_id = data['registration_id']
        user.is_admin = data['is_admin']
        save_changes(user)
        return user, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 409


def remove_user(telegram_id):
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if user:
        User.query.filter_by(telegram_id=telegram_id).delete()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully removed.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()

