import pickle # модуль для сохранения обьектов в файл

################ создание обьекта Member и его методов  #####################

class Member:
    
    def __init__(self, listfields, arg):
        
        ''' создаем словарь пользователя где ключи - имя поля а в значениях - значение этого поля
            мне кажется с словарем будет проще при поиске или изменения любого поля
            чем список где нужно будет помнить индексы да и поле проще добавить в словарь'''

        self.data = dict(zip(listfields,arg))

    def identifier(self):
        '''' возвращает Имя Фамилию одной строкой'''
        return ' '.join([self.data['имя'],self.data['фамилия']]).lower()

    def paramchan(self,key, values):
        '''принимает ключ и новое значение. изменяет значение по ключу
            или создает новую запись если ключа еще нет'''
        self.data[key] = values

    def years(self):
        ''' вернет значение поля возраст'''
        return self.data['возраст']

    def show(self):
        ''' возвращает множество значений словаря в нижнем регистре'''
        return set(map(str.lower, list(self.data.values())))

    def change(self):
        ''' возвращает список ключей'''
        return list(self.data.keys())

    def __str__(self):
        ''' возвращает строку значений'''
        return ' '.join(list(self.data.values()))

######################## часть чтения и записи в файл #############################

def readfile(name):
    try:
        with open(name, 'rb') as f:
            return  pickle.load(f)
    except:
        print('\t\tданных еще не сохранено!\n ')
        return []
        
def savedata(obj,name):
    file = open(name,'wb')
    pickle.dump(obj , file)

################## часть ввода и проверки данных ########################3

def correct_input(text):
    ''' проверка на ввод только букв'''
    name = input(f'{text} > ')
    if name == '*':
        return name 
    while not name.isalpha():
        print('не корректный ввод')
        name = input(f'{text} > ')
    return name.capitalize()
    

def correct_number(text):
    ''' проверка номера'''
    print('номер +7 код номер без пробелов -> ')
    number = input(f'{text} > ')
    while True:
        if number[0] == '+' and number[1:].isdigit() and len(number) == 12:
            return number
        print('не корректный ввод')
        number = input(f'{text} > ')
        
def correct_age(text):
    '''проверка возраста'''
    age = input(f'{text} > ')
    while True:
        if age.isdigit() or age == '*':
            return age
        print('введите цифры !')
        age = input(f'{text} > ')
    
        
def data_input(listfields):
    ''' функция получения данных'''
    list_fun = [correct_input, correct_input, correct_number, correct_age, correct_input]
    return [fun(text) for text, fun in zip(listfields, list_fun)]
        
                

################ функции для работы со справочником ##################
def look(data):
    ''' Просмотр всех записей справочника '''
    for obj in data:
        print(obj)

def search(data,line):
    ''' Поиск по справочнику'''
    trigger = 1 
    for obj in data:
        if line.issubset(obj.show() ):
            trigger = 0
            print(f'\t результат - {obj}')
    if trigger:
        print('совпадений не найдено')

def search_age(data,member):
    for obj in data:
        if obj.identifier().lower() == member.lower():
            print( obj.years())
            return
   

def addmember(listfields, data, name):
    ''' Добавление новой записи '''
    database = data_input(listfields)
    client = ' '.join(database[:2])
    for obj in data:
        client == obj.identifier()
        print('имя и фамилия существуют. выберите другие.')
        return
                      
    memb = Member(listfields, database) # создаем обьект экземпляр класса
    print( 'пользователь добавлен')
    data.append(memb) # добавляем обьект в список
    savedata(data,name) # перезаписываем файл c новыми данными
    

def del_memb(data):
    ''' удаление по имени и фамилии'''
    member = ' '.join(map(str.lower, [input('имя > '), input('фамилия > ')]))
    for i,obj in enumerate(data):
        if obj.identifier() == member:
            data.pop(i)
            savedata(data,name) # перезаписываем файл c новыми данными
            print('удалено')
            return
        
def change(data, member):
    ''' изменение значения по полю  или добавление если еще нет'''
    for obj in data: 
        if  obj.identifier() == member:
            key = input('введите имя поля > ')
            if key not in obj.change():
                print('нет такого поля')
                if input(' создать поле? д\н > ').lower() == 'д':
                    key = input('введите имя поля > ')
                else:
                    return
            values = input('введите значение > ')
            obj.paramchan(key, values)
            break


    
    
################ основная часть #################################



name = 'data.pickle' # имя файла данных
data = readfile(name) # при запуске читаем данные из файла получаем список экземпляров класса
listfields = ['имя','фамилия','номер','возраст','город'] # поля ключей и подсказок ввода

while True:
    
    print('''\n\t\tКоманды для работы со справочником:
    \t\tПросмотр всех записей справочника:  - 1
    \t\tПоиск по справочнику -2
    \t\tДобавление новой записи - 3
    \t\t Удаление записи из справочника по Имени и Фамилии - 4
    \t\tИзменение любого поля в определенной записи справочника - 5 
    \t\tВывод возраста человека (записи) по Имени и Фамилии - 6
     \t\tВыход - 0 \n''')
    
    command = input('Команда: > ')
    
    if command == '1':
        look(data)
    elif command == '2':
        line = set(input('что искать> ').lower().split())#любая подстрока (имя, имя фамилия, фамилия, номер)
        search(data,line)
    elif command == '3':
        print('Введите данные или * при их отсутствии')
        addmember(listfields, data, name)
    elif command == '4':
        del_memb(data)
    elif command == '5':
        member = input('имя фамилия > ').lower()
        change(data, member)
    elif command == '6':
        member = input('имя фамилия > ').lower()
        search_age(data,member)
        
    elif command == '0':
        savedata(data,name)
        print("Работа завершена") 
        raise SystemExit