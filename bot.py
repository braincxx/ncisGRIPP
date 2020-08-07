import datetime
import pytz
from pprint import pprint

from telegram.ext import Updater, Defaults
from telegram.ext import CommandHandler
from telegram.ext import JobQueue

from config import TOKEN


timezone = pytz.timezone('Europe/Moscow')


# /start
def do_start_command(update, context):
    context.user_data['mailing'] = 'normal'
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="привет, тут заглушка, надеюсь это временно"
    )


# /help
def show_help_command(update, context):
    with open('bot_help_message.txt', 'r', encoding='utf8') as f:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=f.read()
        )


# /set_mailing
def set_mailing(update, context):
    if not context.args:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Вы не указали режим, попробуйте еще раз'
        )
    elif context.args[0] == 'no_spam' and context.user_data['mailing'] != 'no_spam':
        context.user_data['mailing'] = 'no_spam'
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Теперь бот не будет слать вам уведомления'
        )
    elif context.args[0] == 'silent' and context.user_data['mailing'] != 'silent':
        context.user_data['mailing'] = 'silent'
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Уведомления с данного момента будут приходить без звука'
        )
    elif context.args[0] == 'normal' and context.user_data['mailing'] != 'normal':
        context.user_data['mailing'] = 'normal'
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Установлен обычный режим уведомлений'
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Такого режима не существует, или вы уже его используете'
        )


def mail_notification(update, context):
    if context.user_data != 'no_spam':
        notification = True
        if context.user_data == 'silent':
            notification = False
        context.bot.send_message(
            chat_id=context.message.chat_id,
            disable_notification=notification,
            text='скоро будет...'
        )
    else:
        pass


updater = Updater(
    token=TOKEN,
    defaults=Defaults(
        parse_mode="HTML",
        disable_web_page_preview=1
    ),
    use_context=True
)

dp = updater.dispatcher
dp.add_handler(
    CommandHandler(
        command='start',
        callback=do_start_command
    )
)
dp.add_handler(
    CommandHandler(
        command='help',
        callback=show_help_command
    )
)
dp.add_handler(
    CommandHandler(
        command='set_mailing',
        callback=set_mailing,
        pass_args=True
    )
)

mailing = JobQueue()
mailing.set_dispatcher(dp)
mailing.run_daily(
    callback=mail_notification,
    time=datetime.time(
        hour=8,
        tzinfo=timezone
    )
)

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
