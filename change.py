from functions import read_from_csv, write_list_to_csv

path = 'phone_db.csv'
coding = 'UTF-8'

from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram import Update

from config import TOKEN


def change():
    '''
        Функция редактирует найденный контакт

    '''

    def get_info(update: Update, context: CallbackContext):

        after_command = context.args
        print(after_command)
        update.message.reply_text(
            "Вы зашли в режим редактирования.\n Введите фамилию и имя контакта, который вы хотите изменить"
            "(через пробел)")

    def edit(update: Update, context: CallbackContext):
        text = update.message.text
        text = text.split()
        text.pop(0)
        data = read_from_csv(path, coding, '|')
        data.append(text)
        write_list_to_csv(path, coding, data)
        update.message.reply_text(f'{text}')
        update.message.reply_text('Контакт успешно изменён и добавлен в БД')

    def get_message(update: Update, context: CallbackContext):
        message = update.message.text
        message = message.split()
        if len(message) == 1:
            message.append(' ')
        find = []
        data = read_from_csv(path, coding, '|')
        print(message)
        for item in data:
            if message[0].capitalize() in item[0] or message[1].capitalize() in item[1]:
                find.append(item)
                # data.remove(item)
                update.message.reply_text(f"Контакт для редактирования найден\n{find}"
                                          f"\nВведите новые данные как в примере\n"
                                          f"'/edit Фамилия Имя Тел Коммент'")
                write_list_to_csv(path, coding, data)
                return None
        else:
            update.message.reply_text(
                f'Неверная команда или контакт не найден, введите команду /info или продолжите поиск')
        return None

    updater = Updater(TOKEN)
    dispetcher = updater.dispatcher

    info_handler = CommandHandler('info', get_info)
    edit_handler = CommandHandler('edit', edit)

    message_handler = MessageHandler(Filters.text, get_message)

    dispetcher.add_handler(info_handler)
    dispetcher.add_handler(edit_handler)
    dispetcher.add_handler(message_handler)

    print('сервер запущен')
    updater.start_polling()
    updater.idle()

change()