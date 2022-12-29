import logging
from add_contact import *
from change import *
from de import *
from ad import *
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
MENU, ADD, ADD_FIRSTNAME, ADD_LASTNAME, ADD_NUMBER, ADD_COMMENT, FIND, START_CHANGE, END_CHANGE, DELETE, END_DELETE = range(11)
# 0     1         2           3             4           5           6       7        8           9         10
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
        'Команда /choice, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n') 
    #return GENDER

def choice(update, _):
    # Список кнопок для ответа  
    reply_keyboard = [['Add contact', 'Find contact', 'Change contact', 'Delete contact']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Я Бот - телефонный справочник.\n'
        'Выбери, что ты хочешь сделать.'
        'Команда /cancel, чтобы завершить.\n\n'
        'Что будем делать?',
        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    return MENU


def parse_choice(update, _):
# Обрабатываем выбор пользователя    
    choice = update.message.text        
    if choice == 'Add contact':
        update.message.reply_text('Вы выбрали "Добавить контакт"\n'        
        'Введите фамилию абонента.\n' , reply_markup=ReplyKeyboardRemove(),)
        return ADD_FIRSTNAME
    elif choice == 'Find contact':
        update.message.reply_text(
        "Вы выбрали 'Найти контакт'.\nВведите фамилию и/или имя контакта, который вы хотите найти"
        "(через пробел)", reply_markup=ReplyKeyboardRemove(),)
        return FIND
    elif choice == 'Delete contact':
        update.message.reply_text(
        "Вы выбрали 'Удалить контакт'.\nВведите фамилию и/или имя контакта, который вы хотите удалить"
        "(через пробел)", reply_markup=ReplyKeyboardRemove(),)
        return DELETE
    elif choice == 'Change contact':
        update.message.reply_text(
        "Вы зашли в режим редактирования.\nВведите фамилию и имя контакта, который вы хотите изменить"
        "(через пробел)", reply_markup=ReplyKeyboardRemove(),)
        return START_CHANGE
    else:
        update.message.reply_text('Выбери, что ты хочешь сделать.'
        'Команда /cancel, чтобы завершить.\n\n',
        reply_markup=ReplyKeyboardMarkup([['Add contact', 'Find contact', 'Change contact', 'Delete contact']], one_time_keyboard=True),)
        return MENU

def message(update, _):  
    update.message.reply_text(
        "что-то пошло не так. попробуйте еще раз")        
    # возвращаемся к меню
    return END_CHANGE
  


if __name__ == '__main__':
    
    updater = Updater(TOKEN)    
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)      

    choice_handler = ConversationHandler(entry_points=[CommandHandler('choice', choice)],
        states = {MENU:[MessageHandler(Filters.regex('^(Add contact|Find contact|Change contact|Delete contact)$'), parse_choice)],
            # ADD:[MessageHandler(Filters.text & ~Filters.command, add_contact), CommandHandler('choice', choice),],
            ADD_FIRSTNAME: [MessageHandler(Filters.text & ~Filters.command, firstname)],
            ADD_LASTNAME: [MessageHandler(Filters.text & ~Filters.command, lastname), CommandHandler('skip', skip_lastname)],
            ADD_NUMBER: [MessageHandler(Filters.text & ~Filters.command, number)],
            ADD_COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],

            FIND:[MessageHandler(Filters.text & ~Filters.command, find_contact),
                CommandHandler('choice', choice),],

            START_CHANGE:[MessageHandler(Filters.text& ~Filters.command, get_message),
                CommandHandler('choice', choice),],
            END_CHANGE: [CommandHandler('edit', edit),
                CommandHandler('choice', choice), 
                MessageHandler(Filters.text & ~Filters.command, message),],  

            DELETE:[MessageHandler(Filters.text & ~Filters.command, del_contact),
                CommandHandler('choice', choice),],
            END_DELETE:[CommandHandler('Yes', check), CommandHandler('No', check),
                CommandHandler('choice', choice),],    
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
  
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(choice_handler)
   

    # Запуск бота
    print('по-е-е-ехали')
    updater.start_polling()
    updater.idle()