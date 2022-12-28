import csv
from typing import List, Optional

def give_int_num(input_string: str,
            min_num: Optional[int] = None,
            max_num: Optional[int] = None) -> int:
    """
    Выпытывает у пользователя число в диапзоне от  min_num до  mах_num:

    Args:
    input_string - предложение ввода

    Returns:
    int - число
    """
    while True:
        try:
            num = int(input(input_string))
            if min_num and num < min_num:
                print(f'Введите больше {min_num-1}')
                continue
            if max_num and num > max_num:
                print(f'Введите меньше {max_num+1}')
                continue
            return num
        except ValueError:
            print('Похоже это не число, попробуте еще раз')


def read_from_csv(path_file: str, coding: str, delim:str ) -> List[List[str]]:
    """
    Считывает csv файл и возвращает строку 

    Args:
    path_file - путь до файла,
    coding - кодировка ('utf-8')
    delim - разделитель (по умолчанию ',')

    Returns:
    List[List[str]] - список
    """ 
    list_file = []
    with open(path_file, 'r', encoding=coding) as r_file:    
        file_reader = csv.reader(r_file, delimiter = delim)   
        for row in file_reader:
            if row != []:
                list_file.append(row) 
    return list_file

def write_list_to_csv(path_file: str, coding: str, list_to_write: List[List[str]]):
    """
    Записывает список в файл 

    Args:
    path_file - путь до файла, 
    coding - кодировка ('utf-8'),
    list_to_write - список для записи
    """
    with open(path_file, 'w', encoding=coding) as w_file:
            file_writer = csv.writer(w_file, delimiter = "|" , lineterminator="\n")
            for row in list_to_write:       
                file_writer.writerow(row) 

def add_list_to_csv(path_file: str, coding: str, list_to_write: List[List[str]]):
    """
    Записывает список в файл 

    Args:
    path_file - путь до файла, 
    coding - кодировка ('utf-8'),
    list_to_write - список для записи
    """
    with open(path_file, 'a', encoding=coding) as w_file:
            file_writer = csv.writer(w_file, delimiter = "|" , lineterminator="\n")
            for row in list_to_write:       
                file_writer.writerow(row) 


def string_to_list(string_line: str) -> List[List[str]]:
    """
    Возвращает список строк разденных по '\\n' в виде списка элементов разделенных по пробелу [[1,2,3],[1,2,3],[1,2,3]] 

    Args:
    string:str - строка для преобразования

    Returns:
    List[List[str]] - список списков вид [[1,2,3],[1,2,3],[1,2,3]] 
    """
    list_file = []
    string = string_line.split('\n')
    for i in string:
        list_file.append(i.split(' '))
    return(list_file)

def list_to_string(list_file: List[List[str]])-> str:
    """
    Возвращает строку вида  item_1\\nitem_2\\n....\\item_n\\n

    Args:
    List[List[str]] - список списков вид [[1,2,3],[1,2,3],[1,2,3]]

    Returns:
    str - строка (item_1\\nitem_2\\n....\\item_n\\n)
    """
    srting =''
    for row in list_file:
        if row[0] != "":   
            srting += row[0]+' '+row[1]+' '+row[2]+' '+row[3]+'\n'        
    return srting[:-1]