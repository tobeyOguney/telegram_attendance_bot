import os

from telegram.ext import Updater, CommandHandler
from bot_commands import *

TOKEN = "915418186:AAEJgzEuaM5HDdF-6Wvwv8cV_lufn8oNJCM"
PORT = 8443

updater = Updater(TOKEN)

# Add Handlers
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('signup', signup))
dp.add_handler(CommandHandler('signupasadmin', signup_as_admin))
dp.add_handler(CommandHandler('startattendance', start_attendance))
dp.add_handler(CommandHandler('checkin', checkin))
dp.add_handler(CommandHandler('checkout', checkout))
dp.add_handler(CommandHandler('getattendance', get_attendance))
dp.add_handler(CommandHandler('endattendance', end_attendance))

# Setup Webhook
updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN)
updater.bot.set_webhook("https://telegram-attendance-bot.herokuapp.com/" + TOKEN)
updater.idle()