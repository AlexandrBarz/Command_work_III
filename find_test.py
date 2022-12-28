import telebot


name_it = ''
surname_it = ''
number_it = ''
email_it = ''
user_id_it = ''
new_number_it = ''



# @bot.message_handler(content_types=['text'])
# def main(message):
#     if message.text == '/main':
#         bot.send_message(message.chat.id, f'Выбери пункт меню, введя соответствующую команду: \n/1 - Показать все записи.\n/2 - Найти номер по фамилии.\n/3 - Найти номер по имени.\n/4 - Поиск по номеру телефона.\n/5 - Добавить новую запись.\n/6 - Изменить существующую запись.\n/7 - Удалить запись.')
#         cr.init_data_base('base_phone.csv')

#     elif message.text == '/1':
#         lg.logging.info('The user has selected item number 1')
#         bot.send_message(message.chat.id, f'{cr.retrive()}')

#     elif message.text == '/2':
#         lg.logging.info('The user has selected item number 2')
#         bot.send_message(message.chat.id, f'Введите фамилию')
#         bot.register_next_step_handler(message, find_surname)

#     elif message.text == '/3':
#         lg.logging.info('The user has selected item number 3')
#         bot.send_message(message.chat.id, f'Введите имя')
#         bot.register_next_step_handler(message, find_name)

#     elif message.text == '/4':
#         lg.logging.info('The user has selected item number 4')
#         bot.send_message(message.chat.id, f'Введите номер  телефона')
#         bot.register_next_step_handler(message, find_number)

#     else:
#         bot.send_message(
#             message.chat.id, f'Я тебя не понимаю. Введи: /help.')


def find_surname(message):
    global surname_it
    surname_it = message.text
    lg.logging.info('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(surname=surname_it)}')


def find_name(message):
    global name_it
    name_it = message.text
    lg.logging.info('User entered: {name_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(name=name_it)}')


def find_number(message):
    global number_it
    number_it = message.text
    lg.logging.info('User entered: {number_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(number=number_it)}')





# поиск (если нужно выгрузить все: result = retrive())
def retrive(firstname='', lastname='', number='', comment=''):
    global db
    result = []
    for row in db:
        if(firstname != '' and row[1] != firstname.title()):
            continue
        if(lastname != '' and row[2] != lastname.title()):
            continue
        if(number != '' and row[3] != number):
            continue
        if(comment != '' and row[3] != comment.lower()):
            continue
        result.append(row)
    if len(result) == 0:
        return f'Контакты не найдены'
    else:
        # выход список списков (переделать в строку с разделителем)
        return result







print('server start')
bot.infinity_polling()