from functions import read_from_csv, write_list_to_csv, list_to_string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from config import TOKEN

def del_contact(update: Update, _):
    find = []
    path = 'phone_db.csv'
    coding = 'UTF-8'
    name = update.message.text.split()        
    if len(name) == 1:
        name.append(" ")    
    phone_list = read_from_csv(path, coding, '|')    
    for char in phone_list:
        if name[0].capitalize() in char[0] or name[1].capitalize() in char[1] or name[1].capitalize() in char[0] or name[0].capitalize() in char[1]:
            find.append(char)                        
            update.message.reply_text(f"Найден контакт:\n {list_to_string(find)}\n"
            "Если хотитe удалить /Yes, иначе /No")
            return 10

    else:
        update.message.reply_text(f"Ничего не удалось найти. Попробуйте еще раз\n"
                "Введите фамилию и/или имя контакта, который вы хотите удалить (через пробел)")
    return 9

def check(update: Update, _):
    path = 'phone_db.csv'
    coding = 'UTF-8' 
    check = update.message.text        
    if check == '/Yes':
        phone_list = read_from_csv(path, coding, '|') 
        for i in range(len(find)): 
            phone_list.remove(find[i])
        write_list_to_csv(path, coding, phone_list)
        update.message.reply_text(f'Удален контакт {list_to_string(find)}')
    
    update.message.reply_text('Выберите что хотите сделать.\n'
            'Команда /cancel, чтобы завершить.\n\n'
            'Что будем делать?',
            reply_markup=ReplyKeyboardMarkup([['Add contact', 'Find contact', 'Change contact', 'Delete contact']], one_time_keyboard=True),)
    return 0

def delete():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('Delete', del_contact))
    updater.dispatcher.add_handler(CommandHandler('Check', check))

    print('сервер запущен')                                      
    updater.start_polling()                                 
    updater.idle()  

if __name__ == '__main__':
    delete()