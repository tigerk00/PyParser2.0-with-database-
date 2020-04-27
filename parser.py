# -*- coding: utf8 -*-

import re
import requests
import sqlite3
from bs4 import BeautifulSoup
import sys
import shutil

print("Made by tigerk00\nGitHub: https://github.com/tigerk00 \n")
conn = sqlite3.connect('bookdata.db')
sql = 'create table if not exists books (id INTEGER PRIMARY KEY   , title TEXT  , price INTEGER , description TEXT  , availability TEXT , author TEXT , pub_house TEXT , language TEXT , release TEXT , number_of_pages TEXT )'
cursor = conn.cursor()
cursor.execute(sql)
conn.close()
while True:
    main_choise = str(input('\n\nВведіть "parser" для того , щоб почати парсинг.\nВведіть "database", для того , щоб почати роботу з базою даних.\nВведіть "exit" для того , щоб закінчити роботу програми.\n'))
    if main_choise == 'parser':
        print("Виберіть  тему книг [1-11]:\n1.Художня література\n2.Книги про бізнес\n3.Суспільство.Країна.Філософія\n4.Історичні книги\n5.Здоров'я.Фітнес.Правильне харчування\n6.Мистецтво.Культура.Фотографія\n7.Література для навчання.Педагогіка\n8.Кулінарія.Їжа та нопої\n9.Наука і техніка\n10.Література по психології\n11.Саморозвиток і мотивація\n")
        choise_theme = int(input('Ваш вибір:  '))
        try:
            if choise_theme <= 11 and choise_theme >=1:
            
                if choise_theme == 1:
                    theme_url = "https://www.yakaboo.ua/knigi/hudozhestvennaja-literatura.html?p="    
                elif choise_theme == 2:
                    theme_url = "https://www.yakaboo.ua/knigi/business-money-economy.html?p="
                elif choise_theme == 3:
                    theme_url = "https://www.yakaboo.ua/knigi/obschestvo-gosudarstvo-filosofija.html?p="
                elif choise_theme == 4:
                    theme_url = "https://www.yakaboo.ua/knigi/istorija.html?p="
                elif choise_theme == 5:
                    theme_url = "https://www.yakaboo.ua/knigi/zdorov-e-fitnes-pravil-noe-pitanie.html?p="
                elif choise_theme == 6:
                    theme_url = "https://www.yakaboo.ua/knigi/iskusstvo-kul-tura-fotografija.html?p="  
                elif choise_theme == 7:
                    theme_url = "https://www.yakaboo.ua/knigi/uchebnaja-literatura-pedagogika.html?p="     
                elif choise_theme == 8:
                    theme_url = "https://www.yakaboo.ua/knigi/kulinarija-eda-i-napitki.html?p="
                elif choise_theme == 9:
                    theme_url = "https://www.yakaboo.ua/knigi/nauka-i-tehnika.html?p="
                elif choise_theme == 10:
                    theme_url = "https://www.yakaboo.ua/knigi/psihologija-i-vzaimootnoshenija.html?p="
                elif choise_theme == 11:
                    theme_url = "https://www.yakaboo.ua/knigi/samorazvitie-motivacija.html?="    
                else:
                    print('Введені некоректні дані')
                
                choise_page= int(input('Виберіть  номер сторінки для парсингу [1-5]:  '))
                if choise_page <=5 and choise_page >=1:
                    url = str(theme_url) + str(choise_page)
                else:
                    print('Ви ввели недопустимі числа або символи')
        except:
            print('Помилка!Спробуйте ще раз , перевірте правильність введених даних.')
        
        

        base_url = 'https://www.yakaboo.ua/ua'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html , 'html.parser')
        container = soup.select_one('div.category-products')
        products = container.find_all('li')




        urls = []
        for product in products:
            url = product.select_one('a.product-name')['href']
            urls.append(base_url + '/' + url.replace('https://www.yakaboo.ua/' , ''))
            
            


        args = []
        for url in urls:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html , 'lxml')
            info_table = soup.find('table' , {'class': 'product-attributes__table'})
        
        
        
        
            name_of_book = soup.select_one('h1').text
            print(name_of_book)
            price_of_book = int(soup.find('span' , {"class": "price"}).find_next('span').text[0:3])
            description_of_book = soup.find('div' , {'class': 'description-shadow'} , 'p').text.replace('\n' , '')
            availability_of_book = soup.find('div' , {'class': 'price-box'}).find_next('div').text.replace('\n' , '').replace('\xa0' , '')
            
            
            
            info_table_author_div = info_table.find_all('td')
            for div in info_table_author_div:
                try:
                    if div.find(text=re.compile("Автор")):
                        thelink = div.text
                        info_table_author = (soup.find('div' , string=thelink).find_next("td").text)
                except:
                    info_table_author = ('-')
                    
            
            
            
            info_table_publishing_house_div = info_table.find_all('td')
            for div in info_table_publishing_house_div:
                try:
                    if div.find(text=re.compile("Видавництво")):
                        thelink = div.text
                        info_table_publishing_house = (soup.find('div' , string=thelink).find_next("td").text)
                except:
                    info_table_publishing_house = ('-')
                        
                
            
            
            
            info_table_language_div = info_table.find_all('td')
            for div in info_table_language_div:
                try:
                    if div.find(text=re.compile("Мова")):
                        thelink = div.text
                        info_table_language = (soup.find('div' , string=thelink).find_next("td").text)
                except:
                    info_table_language = ("-")
                    
            
            
            
            info_table_release_div = info_table.find_all('td')
            for div in info_table_release_div:
                try:
                    if div.find(text=re.compile("Рік видання")):
                        thelink = div.text
                        info_table_release = (soup.find('div' , string=thelink).find_next("td").text)
                    elif div.find(text=re.compile("Год издания")):
                        thelink = div.text
                        info_table_release = (soup.find('div' , string=thelink).find_next("td").text) 
                except:
                    nfo_table_release = ('-')
                    
            
            
            info_table_pages_div = info_table.find_all('div')
            for div in info_table_pages_div:
                try:
                    if div.find(text=re.compile("Кількість сторінок")):
                        thelink = div.text
                        info_table_pages = (soup.find('div' , string=thelink).find_next("td").text)  
                    elif div.find(text=re.compile("Количество страниц")):
                        thelink = div.text
                        info_table_pages = (soup.find('div' , string=thelink).find_next("td").text)
                    
                except:
                    info_table_pages = ('-')
                    
            args.append((name_of_book, price_of_book, description_of_book , availability_of_book , 
                        info_table_author , info_table_publishing_house , info_table_language , 
                        info_table_release , info_table_pages))
            
            
             
                    
        conn = sqlite3.connect('bookdata.db')
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO  books(title ,price,description,availability,author,pub_house,language,release,number_of_pages) VALUES (?,?,?,?,?,?,?,?,?)' , args)
        conn.commit()
        conn.close()        
        
        
        
                
        
        
            
            
                
            
        
        
        
        

    elif main_choise == 'database':
        conn = sqlite3.connect('bookdata.db')
        cursor = conn.cursor()
        command = input('Введіть "filter" для того , щоб побачити дані за фільтром.\nВведіть "all", для того , щоб вивести всі дані парсингу.\nВведіть "full_filter" для того , щоб побачити дані за фільтром із декількома умовами.\nВведіть "exit" , для того , що вийти.\n')
        if command == 'filter':
            choise = int(input("1.Фільтрація за полем id.\n2.Фільтрація за полем price.\n3.Фільтрація за полем author.\n4.Фільтрація за полем title.\n5.Фільтрація за полем release.\n6.Фільтрація за полем number_of_pages.\n"))
            
            if choise == 1:
                id_stroke = int(input('Введіть номер id:\n'))
                sql = ("""
                                SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                FROM books
                                WHERE id = (?) """)
                
                cursor.execute(sql,(id_stroke,))
                results = cursor.fetchall()
            
            elif choise == 2:
                choise_price = input("Введіть 'number' , якщо ви хочете побачити книги по визначеній ціні:\nВведіть 'between' , якщо ви хочете побачити книги в діапазоні цін:\n")
                if choise_price == 'between':
                    print('Введіть межі "від і до" ціни , яка вас цікавить:\n')
                    price1 = int(input("Мінімальна ціна: "))
                    price2 = int(input("\nМаксимальна ціна: "))
                    if price1 < price2:    
                        sql = ("""
                                        SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                        FROM books
                                        WHERE price  BETWEEN (?) AND (?) """)
                        cursor.execute(sql,(price1,price2))
                        results = cursor.fetchall() 
                if choise_price == 'number':
                        price1 = int(input('Значення ціни: '))   
                        sql = ("""
                                        SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                        FROM books
                                        WHERE price  = (?) """)
                        cursor.execute(sql,(price1,))
                        results = cursor.fetchall()
                        
                else:
                    print("Невалідні дані! Спробуйте ще раз.")
            
            elif choise == 3:
                author = str(input("Введіть ім'я чи прізвище автора(або їх частину): "))   
                sql = ("""
                        SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                        FROM books
                        WHERE author  LIKE (?) """)
                cursor.execute(sql,('%'+author+'%',))
                results = cursor.fetchall()
            
            elif choise == 4:
                book = str(input("Введіть назву книги(або частину назви): "))   
                sql = ("""
                        SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                        FROM books
                        WHERE title  LIKE (?) """)
                cursor.execute(sql,('%'+book+'%',))
                results = cursor.fetchall() 
            
            elif choise == 5:
                try:
                    date_release = int(input("Введіть рік видання книг(-и): "))   
                    sql = ("""
                            SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                            FROM books
                            WHERE release = (?) """)
                    cursor.execute(sql,(date_release,))
                    results = cursor.fetchall()
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
                    
            elif choise == 6:
                try:  
                    print('Введіть межі "від і до" кількості сторінок , які вас цікавлять:\n')
                    pages1 = int(input("Мінімальна кількість сторінок: "))
                    pages2 = int(input("\nМаксимальна кількість сторінок: "))
                    if pages1 < pages2:    
                        sql = ("""
                            SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                            FROM books
                            WHERE number_of_pages  BETWEEN (?) AND (?) """)
                        cursor.execute(sql,(pages1,pages2))
                        results = cursor.fetchall()
                    elif pages1 > pages2:
                        print('Неправильно вказані межі "від і до". Спробуйте ще раз.')
                    else:
                        print('Можливо ви ввели дані неправильного типу.')
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            
            
        elif command == 'full_filter':
            choise = int(input("1.Фільтрація за полями title+author+price\n2.Фільтрація за полями release+number_of_pages+price\n3.Фільтрація за полями author+price\n4.Фільтрація за полями author+title\n5.Фільтрація за полями pub_house+price\n6.Фільтрація за полями pub_house+release\n"))
            if choise == 1:
                try:    
                    book = (input('Введіть назву книги(або хоча б частину назви): '))
                    author = (input("Введіть ім'я чи прізвище автора(або їх частину): "))
                    print('Введіть межі "від і до" ціни , яка вас цікавить:\n')
                    price1 = int(input("Мінімальна ціна: "))
                    price2 = int(input("Максимальна ціна: "))
                    if price1<price2:
                    
                        sql = ("""
                                SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                FROM books
                                WHERE title LIKE (?) AND author LIKE (?) AND price BETWEEN (?) AND (?) """)
                        
                        cursor.execute(sql,("%"+str(book)+"%", "%"+str(author)+"%" , price1 ,price2))
                        results = cursor.fetchall()
                    elif price1>price2:
                        print('Неправильно вказані межі "від і до". Спробуйте ще раз.')
                    else:
                        print('Можливо ви ввели дані неправильного типу.')
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            if choise == 2:
                try:    
                    date_release = int(input("Введіть рік видання книг(-и): "))
                    print('Введіть межі "від і до" кількості сторінок , які вас цікавлять:\n')
                    pages1 = int(input("Мінімальна кількість сторінок: "))
                    pages2 = int(input("\nМаксимальна кількість сторінок: "))
                    print('Введіть межі "від і до" ціни , яка вас цікавить:\n')
                    price1 = int(input("Мінімальна ціна: "))
                    price2 = int(input("\nМаксимальна ціна: "))
                    if price1<price2:
                    
                        sql = ("""
                                SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                FROM books
                                WHERE release = (?) AND number_of_pages BETWEEN (?) AND (?) AND price BETWEEN (?) AND (?) """)
                        
                        cursor.execute(sql,(date_release, pages1,pages2 , price1 ,price2))
                        results = cursor.fetchall()
                    elif price1>price2:
                        print('Неправильно вказані межі "від і до". Спробуйте ще раз.')
                    else:
                        print('Можливо ви ввели дані неправильного типу.')
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            
            if choise == 3:
                try:    
                    author = (input("Введіть ім'я чи прізвище автора(або їх частину): "))
                    print('Введіть межі "від і до" ціни , яка вас цікавить:\n')
                    price1 = int(input("Мінімальна ціна: "))
                    price2 = int(input("\nМаксимальна ціна: "))
                    if price1<price2:
                    
                        sql = ("""
                                SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                FROM books
                                WHERE author LIKE (?) AND price BETWEEN (?) AND (?) """)
                        
                        cursor.execute(sql,("%"+author+"%" , price1 ,price2))
                        results = cursor.fetchall()
                    elif price1>price2:
                        print('Неправильно вказані межі "від і до". Спробуйте ще раз.')
                    else:
                        print('Можливо ви ввели дані неправильного типу.')
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            
            if choise == 4:
                try:    
                    author = (input("Введіть ім'я чи прізвище автора(або їх частину): "))
                    book = (input('Введіть назву книги(або хоча б частину назви): '))
                    sql = ("""
                            SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                            FROM books
                            WHERE author LIKE (?) AND title LIKE (?) """)
                        
                    cursor.execute(sql,("%"+author+"%" , "%"+book+"%"))
                    results = cursor.fetchall() 
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            
            if choise == 5:
                try:    
                    pub_house = (input("Введіть назву видавництва(або її частину): "))
                    print('Введіть межі "від і до" ціни , яка вас цікавить:\n')
                    price1 = int(input("Мінімальна ціна: "))
                    price2 = int(input("\nМаксимальна ціна: "))
                    if price1<price2:
                    
                        sql = ("""
                                SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                                FROM books
                                WHERE pub_house LIKE (?) AND price BETWEEN (?) AND (?) """)
                        
                        cursor.execute(sql,("%"+pub_house+"%" , price1 ,price2))
                        results = cursor.fetchall()
                    elif price1>price2:
                        print('Неправильно вказані межі "від і до". Спробуйте ще раз.')
                    else:
                        print('Можливо ви ввели дані неправильного типу.')
                except:
                    print('Невалідні дані! Спробуйте ще раз.')
            
            if choise == 6:
                try:    
                    pub_house = (input("Введіть назву видавництва(або її частину): "))
                    date_release = int(input("Введіть рік видання книг(-и): "))
                    sql = ("""
                            SELECT id , title , price , description , availability , author , pub_house , language , release , number_of_pages
                            FROM books
                            WHERE pub_house LIKE (?) AND release = (?) """)
                        
                    cursor.execute(sql,("%"+pub_house+"%" , str(date_release)))
                    results = cursor.fetchall() 
                except:
                    print('Невалідні дані! Спробуйте ще раз.')

        elif command == 'all':
            sql = ("""
                    SELECT *
                    FROM books """)
                
            cursor.execute(sql)
            results = cursor.fetchall()

        elif command == 'exit':
            sys.exit()


        try:
            for row in results:
                id = row[0]
                title = row[1]
                price = row[2]
                description = row[3]
                availability = row[4]
                author = row[5]
                pub_house = row[6]
                language = row[7]
                release = row[8]
                number_of_pages = row[9]
                print('\nid: ' + str(id) + "\n" +  'Назва книги:' + title + "\n" + 'Ціна:' + str(price) + "\n" + 'Опис:\n' + description + "\n"+'Чи є в наявності: ' + availability + "\n"+'Автор(-и):' + author + "\n"+'Видавництво:' + pub_house + "\n"+'Мова:' + language + "\n"+'Рік видання:' + str(release) + "\n"+'Кількість сторінок:' + str(number_of_pages) + "\n\n\n\n")
        except:
            print()

    elif main_choise == 'exit':
        sys.exit()

    else:
        print('Команда не розпізнана!Спробуйте ще раз.')
    
        
    


