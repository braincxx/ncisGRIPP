import datetime
import logging

from telegram.ext import Updater, Defaults, Filters, CallbackQueryHandler
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from application.repository.users_repository import UsersRepository
from application.repository.notifications_repository import NotificationsRepository
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
    print(user.__dict__)
    if user.tg_logged == 1:
        dp.user_data[user.id]['name'] = user.name
        dp.user_data[user.id]['surname'] = user.surname
        dp.user_data[user.id]['email'] = user.email
        dp.user_data[user.id]['logged'] = True


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
        text="""Вас приветствует бот национальной системы оперативного оповещения. Для полулчеия справки введите /help"""
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


def form_mails_list():
    notes_db = NotificationsRepository.instance().get_all()

    message = '<b>Актуальные новости:</b>\n\n'
    for note in reversed(notes_db):
        message += f"-{note.title}\n"
    return message


def form_mails_keyboard(mails_amount=None):
    notes_db = NotificationsRepository.instance().get_all()

    if mails_amount is None:
        mails_amount = len(notes_db)

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=f"{mail.title}",
            callback_data=f"{mail.id}"
        )] for mail in reversed(notes_db)
    ] + [[InlineKeyboardButton(text='Назад', callback_data='mails_return')]])

    return keyboard_markup


def do_mails(update, context):

    bot_message = form_mails_list()

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Подробнее", callback_data='mails_more'),
         InlineKeyboardButton(text="Закончить", callback_data='mails_end')]
    ])

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=bot_message,
        reply_markup=keyboard_markup
    )


def find_mails(update, context):
    mails_id = update.callback_query.data.replace('mails: ', '')
    print(mails_id)

    notes_db = NotificationsRepository.instance().get_all()

    bot_message = None
    for mails in notes_db:
        if mails.id == mails_id:
            bot_message = f"<b>{mails.title}</b>\n\n" \
                          f"{mails.text}\n"

    context.bot.delete_message(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id
    )

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Назад", callback_data='mails_back'),
         InlineKeyboardButton(text='Показать все', callback_data='mails_to_all')],
         [InlineKeyboardButton(text="Закончить", callback_data='mails_end')]
    ])

    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text=bot_message,
        reply_markup=keyboard_markup
    )


def more_mails(update, context):
    notes_db = NotificationsRepository.instance().get_all()

    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=f"{note.title}",
            callback_data=f"mails: {note.id}"
        )] for note in notes_db
    ] + [[InlineKeyboardButton(text='Назад', callback_data='mails_return')]])

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text='<b>Актуальные новости:</b>\n'
    )

    context.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard_markup
    )


def mails_back(update, context):

    keyboard_markup = form_mails_keyboard()

    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text='<b>Актуальные новости:</b>\n',
        reply_markup=keyboard_markup
    )


def return_to_mails_list(update, context):

    bot_message = form_mails_list()

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Подробнее", callback_data='mails_more'),
         InlineKeyboardButton(text='Показать все', callback_data='mails_show_all')],
         [InlineKeyboardButton(text="Закончить", callback_data='mails_end')]
    ])

    context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=bot_message
    )

    context.bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard_markup
    )


def mails_end(update, context):
    context.bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=None
    )


# /login
def do_login(update, context):
    data = {
        'email': context.user_data['email'],
        'password': context.user_data['password'],
    }
    user = UsersService().instance().find_user_by_credentials(data['email'], data['password']) or False
    del context.user_data['password']

    if user:
        context.user_data['name'] = user.name
        context.user_data['surname'] = user.surname
        user.tg_logged = 1
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Вы авторизованы.'
        )
        UsersRepository.instance().save(user=user)
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
    mails_handler = CommandHandler(command='mails', callback=do_mails)
    more_mails = CallbackQueryHandler(callback=more_mails, pattern='mails_more')
    find_mails = CallbackQueryHandler(callback=find_mails, pattern=r'mails: .+')
    mails_back = CallbackQueryHandler(callback=mails_back, pattern='mails_back')
    return_to_mails_list = CallbackQueryHandler(callback=return_to_mails_list, pattern='mails_return')
    mails_end = CallbackQueryHandler(callback=mails_end, pattern='mails_end')

    dp.add_handler(mails_handler, group=1)
    dp.add_handler(more_mails, group=1)
    dp.add_handler(find_mails, group=1)
    dp.add_handler(mails_back, group=1)
    dp.add_handler(return_to_mails_list, group=1)
    dp.add_handler(mails_end, group=1)

    initialize()
    updater.start_polling()
    updater.idle()
