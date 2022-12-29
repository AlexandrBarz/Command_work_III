from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import TOKEN

import csv

import logging
from typing import Optional, List


from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)



user_data = []


def check_name(name, state_success, state_fail, message_success, message_fail, update):
    if len(name) > 15:
        logger.warning("Слишком много букав :)")
        update.message.reply_text(message_fail)
        return state_fail
    else:
        update.message.reply_text(message_success)
        return state_success


def check_number(input_string: str, state_success, state_fail, update,
                 min_str: Optional[int] = None,
                 max_str: Optional[int] = None):
    try:
        if not input_string.isdigit():
            update.message.reply_text('Вводите только цифры')
            return state_fail
        if len(input_string) < min_str:
            update.message.reply_text(f'Введите строку длиннее {min_str} символов')
            return state_fail
        if len(input_string) > max_str:
            update.message.reply_text(f'Введите строку короче {max_str} символов')
            return state_fail

        update.message.reply_text('И последнее. Описание контакта.')
        return state_success
    except ValueError:
        logger.error('Что пошло не так, попробуйте еще раз')
        return state_fail


# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
FIRSTNAME, LASTNAME, NUMBER, COMMENT = range(4)
FIRSTNAME, LASTNAME, NUMBER, COMMENT = 2,3,4,5

# функция обратного вызова точки входа в разговор
def start(update, _):
    update.message.reply_text(
        'Введите фамилию абонента.\n')
    user_data.clear()

    return FIRSTNAME


# Обрабатываем фамилию
def firstname(update, _):

    user = update.message.from_user
    # Пишем в журнал фамилию пользователя
    last_name = update.message.text
    user_data.append(last_name)
    logger.info("Фамилия %s: %s", user.first_name, last_name)
    # переходим к этапу `LASTNAME`
    return check_name(last_name, LASTNAME, FIRSTNAME, 'Теперь ИМЯ или /skip, если пропустить.', 'Введите еще раз',
                      update)


# Обрабатываем имя
def lastname(update, _):
    # определяем пользователя
    user = update.message.from_user

    # Пишем в журнал сведения об имени
    first_name = update.message.text
    logger.info("Имя %s: %s", user.first_name, first_name)
    user_data.append(first_name)
    # переходим к этапу `NUMBER`
    return check_name(first_name, NUMBER, LASTNAME, 'Великолепно! Введите номер телефона.', 'Введите еще раз', update)


# Обрабатываем команду /skip для имени
def skip_lastname(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал сведения о фото
    logger.info("Пользователь %s не ввел имя.", user.first_name)
    # Отвечаем на сообщение с пропущенным именем
    update.message.reply_text(
        'Теперь введите номер телефона.'
    )
    # переходим к этапу
    return NUMBER


# Обрабатываем номер телефона
def number(update, _):
    # определяем пользователя
    user = update.message.from_user
    # номер телефона
    phone = update.message.text
    # Пишем в журнал сведения о номере
    logger.info("Номер телефона %s: %s", user.first_name, phone)
    user_data.append(phone)
    # переходим к этапу `COMMENT`
    return check_number(phone, COMMENT, NUMBER, update, 3, 13)


# Обрабатываем сообщение с описанием контакта
def comment(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал описание
    comment_text = update.message.text
    logger.info("Комментарий от %s: %s", user.first_name, comment_text)
    user_data.append(comment_text)
    update.message.reply_text('Отлично! Контакт записан.')
    logger.info("Сохраняем в файл пользователя ")
    write_list_to_csv('phone_db.csv', 'UTF-8', user_data)

    # Заканчиваем разговор.
    update.message.reply_text(
        'Я Бот - телефонный справочник.\n'
        'Выбери что ты хочешь сделать.'
        'Команда /cancel, чтобы завершить.\n\n'
        'что будем делать?',
        reply_markup=ReplyKeyboardMarkup([['Add contact', 'Find contact', 'Change contact', 'Delete contact']], one_time_keyboard=True),)
    return 0


def write_list_to_csv(path_file: str, coding: str, list_to_write: List[str]):
    """
    Записывает список в файл
    Args:
    path_file - путь до файла,
    coding - кодировка ('utf-8'),
    list_to_write - список для записи
    """
    with open(path_file, 'a', encoding=coding) as w_file:

        file_writer = csv.writer(w_file, delimiter="|", lineterminator="\n")
        file_writer.writerow(list_to_write)


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь передумал
    logger.info("Пользователь %s передумал.", user.first_name)
    # Отвечаем на отказ
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


def add_contact():
    # Определяем обработчик разговоров `ConversationHandler`

    add_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('add', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            FIRSTNAME: [MessageHandler(Filters.text, firstname)],
            LASTNAME: [MessageHandler(Filters.text, lastname), CommandHandler('skip', skip_lastname)],
            NUMBER: [MessageHandler(Filters.text, number)],
            COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(add_handler)


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    add_contact()

    # Добавляем обработчик разговоров `add_handler`

    # Запуск бота
    updater.start_polling()
    updater.idle()
