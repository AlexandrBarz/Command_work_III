import logging
from config import TOKEN 
from logger import write_log

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    write_log(update, _)
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END
# функция обратного вызова точки входа в разговор
def start(update, _):    
    # Начинаем разговор с вопроса
    write_log(update, _)
    update.message.reply_text(
        'Я Бот-справочник. '
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n') 
    #return GENDER

def choise(update, _):
    # Список кнопок для ответа 
    write_log(update, _)   
    reply_keyboard = [['Add contact', 'Find contact', 'Delete contact', 'Change contact']]
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
    return 1

# Обрабатываем пол пользователя
def last_name(update, _): # не закончено
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал  
    
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    update.message.reply_text(
        'Хорошо. Пришли мне свою фотографию, чтоб я знал как ты '
        'выглядишь, или отправь /skip, если стесняешься.',
        reply_markup=ReplyKeyboardRemove(),
    )    
    return ConversationHandler.END
    # return 2

# def bio(update, _):
#     # определяем пользователя
#     user = update.message.from_user
#     # Пишем в журнал биографию или рассказ пользователя
#     write_log(update, _)
#     logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
#     # Отвечаем на то что пользователь рассказал.
#     update.message.reply_text('Спасибо! Надеюсь, когда-нибудь снова сможем поговорить.')
#     # Заканчиваем разговор.
#     return ConversationHandler.END







if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher


    start_handler = CommandHandler('start', start)
    choise_handler = CommandHandler('start', choise)
    #add_handler = MessageHandler(Filters.regex('^(Add|Find|Delete|Change)$'), last_name)

    choise_handler = ConversationHandler(entry_points=[CommandHandler('choise', choise)],
        states={
            1:[MessageHandler(Filters.regex('^(Add|Find|Delete|Change)$'), last_name)],
            2:[MessageHandler(Filters.text & ~Filters.command, start)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(choise_handler)
    #dispatcher.add_handler(add_handler)


    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    # conv_handler = ConversationHandler( # здесь строится логика разговора
    #     # точка входа в разговор
    #     entry_points=[CommandHandler('start', start)],
    #     # этапы разговора, каждый со своим списком обработчиков сообщений
    #     states={
    #         ADD: [MessageHandler(Filters.regex('^(Add|Find|Delete|Change)$'), gender)],
    #         FIND: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
    #         CHANGE: [
    #             MessageHandler(Filters.location, location),
    #             CommandHandler('skip', skip_location),
    #         ],
    #         DELETE: [MessageHandler(Filters.text & ~Filters.command, bio)],
    #     },
    #     # точка выхода из разговора
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )

    # Добавляем обработчик разговоров `conv_handler`
    # dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(conv_handler)
 
    # dispatcher.add_handler(conv_handler)
    

    # Запуск бота
    updater.start_polling()
    updater.idle()