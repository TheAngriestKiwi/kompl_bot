import sqlite3
from random import randint


def kompl_token():          #функция вытягивания токена из БД
    #создаем локальные переменные
    log = []
    log1 = []
    i = 0
    # подключаем БД
    connection = sqlite3.connect('kompliments.db')
    cursor = connection.cursor()    
    cursor.execute("SELECT * FROM bot") # Достаем токен из БД
    records = (cursor.fetchall())
    cursor.close
    connection.close
    #конвертируем из tuple в list,
    while i< len(records):
        log += records[i]
        i += 1  

    log1= "".join(log) 

    return log1


async def max_number():             #Функция которая находит максимальное кол-во комплиментов в БД
    #создаем локальные переменные
    max_str = ''
    log = []
    i = 0
    # подключаем БД, достаем макс. кол-во комплиментов
    connection = sqlite3.connect('kompliments.db')
    cursor = connection.cursor()    
    cursor.execute("SELECT MAX(id) FROM kompl") 
    records = (cursor.fetchall())
    cursor.close
    connection.close
    #конвертируем из tuple в int, и возвращаем макс. кол-во в int
    while i< len(records):
        log += records[i]
        i += 1     

    max_str =  str(log)
    max_str = max_str.replace('[', '')  
    max_str = max_str.replace(']', '') 
    max_int = int(max_str)

    return  max_int


async def random_number():           #Функция находит рандомное число
    #создаем локальные переменные
    log = []
    i = 0
    # подключаем БД, достаем список уже использованных комплиментов
    connection = sqlite3.connect('kompliments.db')
    cursor = connection.cursor()
    cursor.execute("SELECT rand_number FROM rand_list") 
    records = (cursor.fetchall())
    #выводим из БД в список
    while i< len(records):
        log += records[i]
        i += 1 
    # цикл для вычисления рандомного числа
    while True:
        rand = randint(1,await max_number()) # находит рандомное число от 1 до макс. кол-ва комплиментов
        str_num = str(rand) # конвертируем число в str
        if rand not in log: # проверяем нет ли данного числа в списке уже использованных
            cursor.execute("INSERT INTO rand_list(rand_number) VALUES (?)", (str_num,)) #Заисываем наше число в БД использованных (в конец)
            cursor.execute("DELETE FROM rand_list WHERE rowid = (SELECT rowid FROM rand_list LIMIT 1)") #удаляем верхнюю строку из БД использованных
            connection.commit()
            cursor.close
            connection.close

            return str_num
        else:
            print(rand)


async def gen():            #Функция выбора комплимента из БД
    #создаем локальные переменные
    log = []
    log1 = []
    i = 0
    # подключаем БД
    connection = sqlite3.connect('kompliments.db')
    cursor = connection.cursor()    
    cursor.execute("SELECT kom FROM kompl WHERE id = ?",(await random_number(),)) #достаем комплимент по id(где id это наше рандомное число которое мы находили выше)
    cursor.close
    connection.close
    records = (cursor.fetchall())
    #конвертируем из tuple в list,
    while i< len(records):
        log += records[i]
        i += 1  

    log1= "".join(log) 

    return log1