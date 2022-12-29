from functions import read_from_csv, write_list_to_csv, list_to_string
from telegram import Update
from telegram.ext import Updater, CommandHandler
from config import TOKEN

find = []

def del_contact(update: Update, _):
    name = update.message.text.split()        
    if len(name) == 1:
        name.append(" ")    
    phone_list = read_from_csv('phone_db.csv', 'UTF-8', '|')    
    for char in phone_list:
        if name[0].capitalize() in char[0] or name[1].capitalize() in char[1] or name[1].capitalize() in char[0] or name[0].capitalize() in char[1]:
            find.append(char)                        
            update.message.reply_text(f"Найден контакт:\n {list_to_string(find)}\n"
                "Если хотитe удалить /Yes, иначе /No")
            return
    else:
        update.message.reply_text(f"Ничего не удалось найти. Попробуйте еще раз\n"
        "Введите фамилию и/или имя контакта, который вы хотите удалить (через пробел)")

def check(update: Update, _): 
    check = update.message.text        
    if check == '/Yes':
        phone_list = read_from_csv('phone_db.csv', 'UTF-8', '|') 
        for i in range(len(find)): 
            phone_list.remove(find[i])
        write_list_to_csv('phone_db.csv', 'UTF-8', phone_list)
        update.message.reply_text(f'Удален контакт {list_to_string(find)}')
    
def delete():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('Delete', del_contact))
    updater.dispatcher.add_handler(CommandHandler('Yes', check))

    print('сервер запущен')                                      
    updater.start_polling()                                 
    updater.idle()  

if __name__ == '__main__':
    delete()