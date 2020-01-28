import requests


BASE_URL = 'http://0.0.0.0:41262'
PASSWORD = "accountability"


def start(bot, update):
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text="Hello, World!")

def signup(bot, update):
    data = dict(
        first_name=update.message.to_dict()['from'].get('first_name', ''),
        last_name=update.message.to_dict()['from'].get('last_name', ''),
        telegram_id=update.message.to_dict()['from']['id'],
        registration_id=update.message.text.split()[1],
        is_admin=False
    )
    response = requests.post(url=BASE_URL+"/user/", data=data).json
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])

def signup_as_admin(bot, update):
    if update.message.text.split()[2].lower != PASSWORD:
        bot.send_message(chat_id="update.message.to_dict()['from']['id']", text="Incorrect password, please try again.")
        return
    data = dict(
        first_name=update.message.to_dict()['from'].get('first_name', ''),
        last_name=update.message.to_dict()['from'].get('last_name', ''),
        telegram_id=update.message.to_dict()['from']['id'],
        registration_id=update.message.text.split()[1],
        is_admin=False
    )
    response = requests.post(url=BASE_URL+"/user/", data=data).json
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])

def start_attendance(bot, update):
    data = dict(
        group_id=update.message.to_dict()["chat"]["id"],
        alias=update.message.text.split()[1],
        min_duration=update.message.text.split()[2],
        is_open=True
    )
    response = requests.post(url=BASE_URL+"/attendance/", data=data)
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])

def get_attendance(bot, update):
    message_response = list()

    data=dict(
        group_id=update.message.to_dict()["chat"]["id"],
        alias=update.message.text.split()[1]
    )

    checkin_response = requests.get(url=BASE_URL+"/attendance/checkedin_users/{group_id}/{alias}".format(**data))
    checkout_response = requests.get(url=BASE_URL+"/attendance/checkedout_users/{group_id}/{alias}".format(**data))

    user_ids_checkin = [user['telegram_id'] for user in checkin_response]
    user_ids_checkout = [user['telegram_id'] for user in checkout_response]

    for user_id in user_ids_checkout:
        if user_id in user_ids_checkin:
            message_response.append(
                "{registration_id} {first_name} {last_name}".format(**checkout_response[user_id])
                )
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text="\n".join(message_response))

def end_attendance(bot, update):
    data=dict(
        group_id=update.message.to_dict()["chat"]["id"],
        alias=update.message.text.split()[1]
    )
    response = requests.put(url=BASE_URL+"/attendance/{group_id}/{alias}".format(**data))
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])

def checkin(bot, update):
    data = dict(
        telegram_id=update.message.to_dict()['from']['id']
    )
    response = requests.post(url=BASE_URL+"/attendance/checkin", data=data)
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])

def checkout(bot, update):
    data = dict(
        telegram_id=update.message.to_dict()['from']['id']
    )
    response = requests.post(url=BASE_URL+"/attendance/checkin", data=data)
    bot.send_message(chat_id=update.message.to_dict()['from']['id'], text=response['message'])