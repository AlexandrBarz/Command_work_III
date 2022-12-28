# Код Анны

from telegram import Update
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




# def check_name(name, state_success, state_fail, message_success, message_fail, update):
#     if len(name) > 15:
#         logger.warning("Слишком много букав :)")
#         update.message.reply_text(message_fail)
#         return state_fail
#     else:
#         update.message.reply_text(message_success)
#         return state_success


# def check_number(input_string: str, state_success, state_fail, update,
#                  min_str: Optional[int] = None,
#                  max_str: Optional[int] = None):
#     try:
#         if not input_string.isdigit():
#             update.message.reply_text('Вводите только цифры')
#             return state_fail
#         if len(input_string) < min_str:
#             update.message.reply_text(f'Введите строку длиннее {min_str} символов')
#             return state_fail
#         if len(input_string) > max_str:
#             update.message.reply_text(f'Введите строку короче {max_str} символов')
#             return state_fail

#         update.message.reply_text('И последнее. Описание контакта.')
#         return state_success
#     except ValueError:
#         logger.error('Что пошло не так, попробуйте еще раз')
#         return state_fail

user_data = []

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
FIRSTNAME, LASTNAME = range(2)


# функция обратного вызова точки входа в разговор
def start(update, _):
    update.message.reply_text(
        'Введите имя контакта для поиска.\n')
    user_data.clear()

    return FIRSTNAME



# Обрабатываем имя (МОЯ ПРАВКА)

def firstname(update, _):
    # определяем пользователя
    user = update.message.from_user

    # Пишем в журнал сведения об имени
    first_name = update.message.text
    logger.info("Имя %s: %s", user.first_name, first_name)
    user_data.append(first_name)
    return user_data


def find_by_firstname():
    
    file_path = 'phone_db.csv'
    read_data = read_from_csv(file_path, 'UTF-8')
    pb = string_to_list(read_data)
    temp = []
    firstname = ''
      
    for i in range(len(pb)):
        if firstname == pb[i]:
            temp.append(pb[i])
                
    if len(temp) == 0:
        update.message.reply_text(f'Попробуй поискать еще разок\n')
        return state_fail
    else: 
        update.message.reply_text(f'Найдено:\n', string_to_list(temp))    
        return state_success

    
    # Обрабатываем фамилию
def lastname(update, _):

    user = update.message.from_user
    # Пишем в журнал фамилию пользователя
    last_name = update.message.text
    user_data.append(last_name)
    logger.info("Фамилия %s: %s", user.first_name, last_name)
    # переходим к этапу `LASTNAME`
    return check_name(last_name, LASTNAME, FIRSTNAME, 'Теперь ИМЯ или /skip, если пропустить.', 'Введите еще раз',
                      update)

  
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
    # Заканчиваем разговор.
    return ConversationHandler.END



# # Обрабатываем сообщение с описанием контакта
# def comment(update, _):
#     # определяем пользователя
#     user = update.message.from_user
#     # Пишем в журнал описание
#     comment_text = update.message.text
#     logger.info("Комментарий от %s: %s", user.first_name, comment_text)
#     user_data.append(comment_text)
#     # update.message.reply_text('Отлично! Контакт записан.')
#     # logger.info("Сохраняем в файл пользователя ")
#     # write_list_to_csv('phone_db.csv', 'UTF-8', user_data)

   





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


def find_contact():
    # Определяем обработчик разговоров `ConversationHandler`

    find_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('find', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            FIRSTNAME: [MessageHandler(Filters.text, firstname), CommandHandler('skip', skip_firstname)],
            LASTNAME: [MessageHandler(Filters.text, lastname), CommandHandler('skip', skip_lastname)],
            # NUMBER: [MessageHandler(Filters.text, number), CommandHandler('skip', skip_number)],
            # COMMENT: [MessageHandler(Filters.text, comment), CommandHandler('skip', skip_comment)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(find_handler)


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    find_contact()

    # Добавляем обработчик разговоров `find_handler`

    # Запуск бота
    updater.start_polling()
    updater.idle()







# Предыдущая функция
from functions import read_from_csv, string_to_list

def find():
    file_path = 'phone_db.csv'
    read_data = read_from_csv(file_path, 'UTF-8')
    pb = string_to_list(read_data)
    
    # Данная функция реализует поиск существующего контакта и выводит результат
    choice = int(input("\n1. Фамилия\n2. Имя\n3. Номер телефона\n4. Коммментарий)\
  \nВыберите критерий поиска: >"))
    query = ""
    temp = []

    if choice == 1:
        # Реализация поиска по имени контакта
        query = str(input("Введите фамилию контакта для поиска: "))

    elif choice == 2:
        # Реализация поиска по фамилии контакта
        query = str(input("Введите имя контакта для поиска: "))

    elif choice == 3:
        # Реализация поиска по номеру телефона контакта
        query = int(input("Введите номер телефона контакта для поиска: "))

    elif choice == 4:
        # Реализация поиска по комментарию к контакту
        query = str(input("Введите комментарий к контакту для поиска: "))
    else:
        print("Неверный критерий поиска, дружок!")
        return

    for i in range(len(pb)):
        if query == pb[i][choice - 1]:
            temp.append(pb[i])
            
    
    if len(temp) == 0:
        print(f"Попробуй поискать еще разок\n {string_to_list(pb)}")
    else: 
        print('Найдено:\n', string_to_list(temp))

    return 
