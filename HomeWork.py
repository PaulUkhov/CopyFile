from csv import DictWriter, DictReader
from os.path import exists

class NameError(Exception):
        # Класс для пользовательского исключения, указывающего на ошибку ввода имени или фамилии.
        def __init__(self, txt):
            self.txt = txt
def get_data():
    """
    Создание и возвращение данных о пользователе.
    """
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            last_name = input("Введите фамилию: ")
            if len(last_name) < 5:
                raise NameError("Слишком короткая фамилия")
        except NameError as err:
            print(err)
        else:
            flag = True
    phone = "+73287282037"
    return [first_name, last_name, phone]

def create_file(filename):
    """
    Создание нового файла и запись в него заголовков колонок.
    Если файл существует, он будет перезаписан.
    """
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()

def read_file(filename):
    """
    Чтение содержимого файла и возвращение его в виде списка словарей.
    """
    with open(filename, 'r', encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)

def write_file(filename, lst):
    """
    Чтение содержимого файла, добавление новой записи и перезапись файла.
    """
    res = read_file(filename)
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    res.append(obj)
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)

def row_search(filename):
    """
    Поиск записи по фамилии и вывод её на экран.
    Если запись не найдена, вывод соответствующего сообщения.
    """
    last_name = input("Введите фамилию: ")
    res = read_file(filename)
    for row in res:
        if last_name == row['Фамилия']:
            print(row)
            return row
    return "Запись не найдена"

def delete_row(filename):
    """
    Удаление записи по фамилии и перезапись файла без этой записи.
    """
    last_name = input("Введите фамилию для удаления: ")
    res = read_file(filename)
    new_res = [row for row in res if row['Фамилия'] != last_name]
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(new_res)
    print("Запись удалена, если она существовала")
    

def change_row(filename):
    """
    Поиск записи по фамилии и изменение её данных.
    Если запись не найдена, вывод соответствующего сообщения.
    """
    last_name = input("Введите фамилию для изменения: ")
    res = read_file(filename)
    found = False
    for row in res:
        if row['Фамилия'] == last_name:
            row['Имя'] = input("Введите новое имя: ")
            row['Телефон'] = input("Введите новый телефон: ")
            found = True
            break
    if not found:
        print("Запись не найдена")
        return
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)
    print("Запись изменена")

filename = 'phone.csv'

def copy_file(src_filename, dest_filename):
    """
    Копирование данных из одного файла в другой.
    """
    if not exists(src_filename):
        print("Исходный файл не существует.")
        return
    data = read_file(src_filename)
    with open(dest_filename, 'w', encoding='utf-8') as data_file:
        f_w = DictWriter(data_file, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(data)
    print(f"Данные скопированы из {src_filename} в {dest_filename}.")

def main():
    """
    Основная функция, обрабатывающая команды пользователя для взаимодействия с телефонной книгой.
    """
    if not exists(filename):
        create_file(filename)
        print("Файл не существует, создайте его")

    while True:
        command = input("Введите команду (q - выход, w - запись, r - чтение, f - поиск, d - удаление, c - изменение): ")
        if command == 'q':
            break
        elif command == 'w':
            write_file(filename, get_data())
        elif command == 'r':
            print(read_file(filename))
        elif command == 'f':
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(row_search(filename))
        elif command == 'd':
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            delete_row(filename)
        elif command == 'c':
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            change_row(filename)

main()

