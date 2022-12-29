from functions import read_from_csv, write_list_to_csv

path = 'phone_db.csv'
coding = 'UTF-8'

from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram import Update, ReplyKeyboardMarkup

from config import TOKEN

MENU = 0
END_CHANGE = 8

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
    print(text)
    data = read_from_csv('phone_db.csv', 'UTF-8', '|')
    data.append(text)
    write_list_to_csv('phone_db.csv', 'UTF-8', data)
    update.message.reply_text(f'{text}\nКонтакт успешно изменён и добавлен в БД\n'
        'Выбери, что ты хочешь сделать.\n'
        'Команда /cancel, чтобы завершить.\n',
        reply_markup=ReplyKeyboardMarkup([['Add contact', 'Find contact', 'Change contact', 'Delete contact']], one_time_keyboard=True),)
    return MENU

def get_message(update: Update, context: CallbackContext):
    message = update.message.text
    message = message.split()
    if len(message) == 1:
        message.append(' ')
    find = []
    data = read_from_csv('phone_db.csv', 'UTF-8', '|')
    print(message)
    for item in data:
        if message[0].capitalize() in item[0] or message[1].capitalize() in item[1]:
            find.append(item)
            data.remove(item)
            update.message.reply_text(f"Контакт для редактирования найден\n{find}"
                                        f"\nВведите новые данные как в примере\n"
                                        f"'/edit Фамилия Имя Тел Коммент'")
            write_list_to_csv('phone_db.csv', 'UTF-8', data)
            return END_CHANGE
    else:
        update.message.reply_text(
            f'Неверная команда или контакт не найден, введите команду /choise чтобы вернуться к меню')
    return END_CHANGE

def change():
    '''
        Функция редактирует найденный контакт

    '''
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


if __name__ == '__main__':
    change()