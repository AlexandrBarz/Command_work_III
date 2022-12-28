import logging
from add_contact import *
from change import *
from config import TOKEN 

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Определяем константы этапов разговора
MENU, ADD, ADD_FIRSTNAME, ADD_LASTNAME, ADD_NUMBER, ADD_COMMENT, FIND, START_CHANGE, END_CHANGE, DELETE = range(10)
# 0     1         2           3             4           5           6       7        8           9
# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s завершил работу.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Работа завершена', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END
# функция обратного вызова точки входа в разговор
def start(update, _):    
    # Начинаем разговор
    update.message.reply_text(
        'Я Бот-справочник. '
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n') 
    #return GENDER

def choise(update, _):
    # Список кнопок для ответа  
    reply_keyboard = [['Add contact', 'Find contact', 'Change contact', 'Delete contact']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Я Бот - телефонный справочник.\n'
        'Выбери что ты хочешь сделать.'
        'Команда /cancel, чтобы завершить.\n\n'
        'что быдем делать?',
        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    return MENU


def parse_choise(update, _):
# Обрабатываем выбор пользователя    
    choise = update.message.text        
    if choise == 'Add contact':
        update.message.reply_text('Вы выбрали Добавить контакт\n'        
        'Введите фамилию абонента.\n')
        return ADD_FIRSTNAME
    elif choise == 'Find contact':
        update.message.reply_text(
        "Вы выбрали 'Найти контакт'.\n Введите фамилию и/или имя контакта, который вы хотите найти"
        "(через пробел)")
        return FIND
    elif choise == 'Delete contact':
        return DELETE
    elif choise == 'Change contact':
        update.message.reply_text(
        "Вы зашли в режим редактирования.\n Введите фамилию и имя контакта, который вы хотите изменить"
        "(через пробел)")
        return START_CHANGE
    else:        
        return MENU

def message(update, _):  
    update.message.reply_text(
        "что-то пошло не так. попробуйте еще раз")        
    # возвращаемся к меню
    return END_CHANGE

def delete(update, _):
    # костыль  #заглушка
    update.message.reply_text('Вы выбрали удалить контакт'
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n')
    # возвращаемся к меню
    return MENU
  

def find(update, _):  #заглушка
    update.message.reply_text('Вы выбрали поиск контакта')
    # возвращаемся к меню    
    return MENU




if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)      

    choise_handler = ConversationHandler(entry_points=[CommandHandler('choise', choise)],
        states = {MENU:[MessageHandler(Filters.regex('^(Add contact|Find contact|Change contact|Delete contact)$'), parse_choise)],
            # ADD:[MessageHandler(Filters.text & ~Filters.command, add_contact),
            #     CommandHandler('choise', choise),],
            ADD_FIRSTNAME: [MessageHandler(Filters.text, firstname)],
            ADD_LASTNAME: [MessageHandler(Filters.text, lastname), CommandHandler('skip', skip_lastname)],
            ADD_NUMBER: [MessageHandler(Filters.text, number)],
            ADD_COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],

            FIND:[MessageHandler(Filters.text, find),
                CommandHandler('choise', choise),],


            START_CHANGE:[MessageHandler(Filters.text, get_message),
                CommandHandler('choise', choise),],
            END_CHANGE: [CommandHandler('edit', edit),
                CommandHandler('choise', choise), 
                MessageHandler(Filters.text, message),],    




            DELETE:[MessageHandler(Filters.text & ~Filters.command, delete),
                CommandHandler('choise', choise),],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

  
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(choise_handler)
    #dispatcher.add_handler(test_handler)
 
    

    # Запуск бота
    print('по-е-е-ехали')
    updater.start_polling()
    updater.idle()