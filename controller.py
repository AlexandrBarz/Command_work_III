import logging
import add_contact, change
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
MENU, ADD, FIND, CHANGE, DELETE = range(5)

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
        return ADD 
    elif choise == 'Find contact':
        return FIND
    elif choise == 'Delete contact':
        return DELETE
    elif choise == 'Change contact':
        return CHANGE
    else:        
        return MENU
    

def add(update, _):  
    add_contact.add_contact()
    # возвращаемся к меню
    return MENU 


def change_h(update, _):    
    change.change()
    # возвращаемся к меню    
    return MENU


def find(update, _):
    # костыль
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Вы выбрали найти контакт'
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n')
    # возвращаемся к меню
    return MENU

def delete(update, _):
    # костыль
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Вы выбрали удалить контакт'
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n')
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
            ADD:[MessageHandler(Filters.text & ~Filters.command, add),
                CommandHandler('choise', choise),],
            FIND:[MessageHandler(Filters.text & ~Filters.command, find),
                CommandHandler('choise', choise),],
            CHANGE:[MessageHandler(Filters.text & ~Filters.command, change_h),
                CommandHandler('choise', choise),],
            DELETE:[MessageHandler(Filters.text & ~Filters.command, delete),
                CommandHandler('choise', choise),],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    #test_handler = MessageHandler(Filters.regex('^(Add contact|Find|Delete|Change)$'), parse_choise)
    #parse_handler = 

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(choise_handler)
    #dispatcher.add_handler(test_handler)
    #dispatcher.add_handler(parse_handler)

    

    # Запуск бота
    updater.start_polling()
    updater.idle()