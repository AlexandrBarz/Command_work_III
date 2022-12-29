from functions import read_from_csv, list_to_string
from telegram import Update


def find(update: Update, _):
    name = update.message.text.split()        
    if len(name) == 1:
        name.append(" ")
    find = [['фамилия','имя','телефон','комментарий']]
    phone_list = read_from_csv('phone_db.csv', 'UTF-8', '|')    
    for char in phone_list:
        if name[0].capitalize() in char[0] or name[1].capitalize() in char[1] or name[1].capitalize() in char[0] or name[0].capitalize() in char[1]:
            find.append(char)                        
            update.message.reply_text(f"Найден контакт:\n {list_to_string(find)}")
            return 0
    else:
        update.message.reply_text(f"Ничего не удалось найти. Попобуете еще раз\n"
                "Введите фамилию и/или имя контакта, который вы хотите найти (через пробел)")
    return 6