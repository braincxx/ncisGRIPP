import datetime
import logging

from telegram.ext import Updater, Defaults, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from application.repository.users_repository import UsersRepository
from application.service.users import UsersService

import config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def initialize():
    users_db = UsersRepository().instance().get_all()
    for user in users_db:
        init_user(user)


def init_user(user):
    if user.tg_logged == 1:
        dp[user.id]['name'] = user.name
        dp[user.id]['surname'] = user.surname
        dp[user.id]['email'] = user.email
        dp[user.id]['logged'] = True


# /start
def do_start_command(update, context):
    mailing = updater.job_queue
    mailing.run_daily(
        callback=mail_notification,
        time=datetime.time(18, 48, 10),
        context=context
    )

    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="""Вас приветствует бот национальной системы оперативного оповещения.
Моя задача отправлять актуальные уведомления на тему г
"""
    )


# /help
def show_help_command(update, context):
    with open('bot_help_message.txt', 'r', encoding='utf8') as f:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=f.read()
        )


def mail_notification(context):
    for user_id in dp.user_data.keys():
        context.bot.send_message(
            chat_id=user_id,
            text='*not yet implemented*'
        )


def show_all_mails(update, context):



# /login
def do_login(update, context):
    data = {
        'email': context.user_data['email'],
        'password': context.user_data['password'],
    }
    user = UsersService().instance().find_user_by_credentials(data['email'], data['password'])
    del context.user_data['password']

    if user:
        context['name'] = user.name
        context['surname'] = user.surname
        user.tg_logged = 1
        UsersRepository.save(user)
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Неверный адрес электронной почты или пароль"
        )


def login_delete_password(update, context):
    context.bot.deleteMessage(
        chat_id=update.message.chat_id,
        message_id=update.message.message_id,
    )
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="<b>*сообщение с паролем удалено*</b>"
    )


def do_login_at_once(update, context):
    if 'logged' in context.user_data.keys() and context.user_data['logged']:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Вы уже авторизованы"
        )
        if len(context.args) == 2:  # Removing message in case if password was there
            context.bot.deleteMessage(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
            )
        return ConversationHandler.END
    if len(context.args) > 2:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="К сожалению, команда принимает максимум два параметра - электронную почту и пароль"
        )
        return ConversationHandler.END
    try:
        context.user_data['email'] = context.args[0]
        try:
            context.user_data['password'] = context.args[1]
            login_delete_password(update, context)
            do_login(update, context)
            return ConversationHandler.END
        except IndexError:
            context.bot.sendMessage(
                chat_id=update.message.chat_id,
                text="Введите пароль"
            )
            return PASSWORD
    except IndexError:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Введите адрес электронной почты"
        )
        return EMAIL


def do_login_email(update, context):
    context.user_data['email'] = update.message.text
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Введите пароль"
    )
    return PASSWORD


def do_login_password(update, context):
    context.user_data['password'] = update.message.text
    login_delete_password(update, context)
    do_login(update, context)
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(
        token=config.TOKEN,
        defaults=Defaults(
            parse_mode="HTML",
            disable_web_page_preview=1
        ),
        use_context=True
    )

    dp = updater.dispatcher
    # /start
    dp.add_handler(
        CommandHandler(
            command='start',
            callback=do_start_command
        )
    )
    # /help
    dp.add_handler(
        CommandHandler(
            command='help',
            callback=show_help_command
        )
    )
    # /login
    EMAIL, PASSWORD = range(2)
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('login', callback=do_login_at_once)],
            states={
                EMAIL: [MessageHandler(Filters.text, callback=do_login_email)],
                PASSWORD: [MessageHandler(Filters.text, callback=do_login_password)]
            },
            fallbacks=[]
        )
    )
    # /all_mails
    dp.add_handler(CommandHandler('all_mails', callback=show_all_mails))

    initialize()
    updater.start_polling()
    updater.idle()
