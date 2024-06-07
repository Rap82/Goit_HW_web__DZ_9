import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://quotes.toscrape.com/'

authors_info = []  # Список в який будемо добавляти інформацію по авторам з сайту який будемо парсити .В нашому випадку 'https://quotes.toscrape.com/'
quotes_info = []  # Список в який будемо добавляти інформацію по цитатам з сайту який будемо парсити .В нашому випадку 'https://quotes.toscrape.com/'



def quotes(url):
    """ Функція парсить інформацію з цитатами
    Функція яка приймає один аргумент посилання на сайт який будемо парсати , проходиться по всім його сторінкам і за вказаними тегами формує список 
    елементи якого є словники де ключами будуть теги які парсимо а значеннями рядки які йдуть за цими тегами ."""
    response = requests.get(url) # Метод *requests.get(*параметри(дивись документацію)) бібліотеки *requests робить запит за вказаними параметрами і повертає результат 
                                 # Примітка : в нашому випадку перевіряємо чи відповідає сайт який будемо парсати . url='https://quotes.toscrape.com/' 
                                        # Якщо ресурс доступний поверне *<Response [200]>

    soup = BeautifulSoup(response.text, 'html.parser') # Повертає обєкт *<class 'bs4.BeautifulSoup'> який містить код сторінки типу html

    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")] # Формуємо список з цитат (тег 'span' - контейнер з текстом, між ними розміщається текст який відображається на сайті. )
                                                                                 # Примітка: цей запис буде повертати весь текст між *<span class="text" > "Якийсь текст.... " </span>
    
    authors_list = [author.text for author in soup.find_all('small', class_="author")]# Формуємо список з авторів  ( тег 'small' - контейнер з коротким текстом, зазвичай інформація з авторми, ліцензіями, короткими коментарями )
                                                                                      # Примітка: цей запис буде повертати весь текст між  < small class="author" > "Якийсь коротки текст.... " </small>
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")] # Формуємо список з тегів  ( тег 'div'  використовується, щоб групувати блоки інформації та форматувати її за допомогою CSS. 
                                                                                                                 # ЦЕ блоковий елемент і призначений для виділення фрагмента документа з метою зміни виду вмісту. )
    for quote, author, tags in zip(quotes_list, authors_list, tags_list): # Цикл в якому будемо з елементів наших сформованих списків *(quotes_list, authors_list, tags_list) формувати кортежі, за допомогою функції *zip(*ітерабельні_елементи(списки,рядки тощо ) )- формує і повертає кортежі.
                                                                          # Далі формуємо словник де одноїменим ключам присфоювати відповідний значення кортежу . 
                                                                          # Сформований відповідно словкник добавляємо в список *quotes_info
        quotes_info.append({'tags': tags, 'author': author, 'quote': quote,})
    
   
    next_page = soup.find('li', class_='next') # За допомогою методу *зміна_що_містить_копію_коду_html.find('li', class_='next') шукаємо елементи що містять вказані параметри .
                                            # В нашому випадку якщо в коді сторінки міститься теги 'li' і 'next' це вказує що сайт містить більше ніж одну html сторінку.
    if next_page: # Умова в якій перевіряємо чи next_page не дорвнює None(якщо дорівнює значить *soup.find('li', class_='next')- ненайшов більше таких тегів -значит це отсанн сторінка сайту)
                  # Якщо поточна сторінка містить теги 'li', class_='next' шукаємо теги які будуть вказувати а дересу наступної сторінки html
        next_page_link = next_page.find('a')['href'] # шукаємо за тегами 'a' і 'href' відносний шлях який вказує на наступну сторінку в нашому випадку вигляд буде *next_page_link == "/page/2/"
        next_page_url = BASE_URL + next_page_link # Склеюємо дві стрічки (перша це посилання на сайт друга це відносний шлях до конкретної сторінки html)- отримуємо повне посилання на конкретну сторінку
                                                  # В нашому випадку *next_page_url ==  https://quotes.toscrape.com//page/2/
        quotes(next_page_url)  # Викликаємо рекурсивно функцію quotes(next_page_url) - де *next_page_url - буде містити повнийшлях до поточної сторніки. 
                               # Повторно пройдемось по поточній сторінці . Добавимо всю потрібну інформацію в *quotes_info і перевіримо чи є наступна .
                               # Якщо є то все знову по колу через рекурсивний виклки *quotes(next_page_url). Як тільки сторінки закінчаться *next_page = soup.find('li', class_='next') - поверне *None
                               #  Умова *if next_page: - невиконається і почне виконуватись подальший код програми.


def authors(url):
    """ Функція парсить інформацію з авторами 
    Функція яка приймає один аргумент посилання на сайт який будемо парсати , проходиться по всім його сторінкам і за вказаними тегами формує список 
    елементи якого є словники де ключами будуть теги які парсимо а значеннями рядки які йдуть за цими тегами ."""
    # Примітка : Пояснення до коду цієї фугкції аналогічно функції *quotes(url) просто перевіряєм за іншими тегами і формуємо інший список *authors_info
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_about_author = soup.find_all('a', string='(about)')
    for link in link_about_author:
        new_url = BASE_URL + link['href']
        response = requests.get(new_url)
        soup_author = BeautifulSoup(response.text, 'html.parser')
        fullname = soup_author.find('h3', class_="author-title").text
        born_date = soup_author.find('span', class_="author-born-date").text
        born_location = soup_author.find('span', class_="author-born-location").text
        description = soup_author.find('div', class_="author-description").text.strip()
        authors_dict = {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
            }
        authors_info.append(authors_dict)
    
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_link = next_page.find('a')['href']
        next_page_url = BASE_URL + next_page_link
        authors(next_page_url)  # Викликаємо рекурсивно функцію *authors(next_page_url)


def write_json(filename, info):
    """Функція запису даних в формат *імя_файла.jason
    Отримує два аргументи , *filename - імя файлу  і *info - дані для запису в файл з іменем що міститься в *filename"""
    with open(filename, 'w', encoding='utf-8') as fd:
        json.dump(info, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    quotes(BASE_URL)  # Стартуем с первой страницы цитат
    write_json('quotes.json', quotes_info)  # Сохраняем цитаты в JSON
    authors(BASE_URL)  # Стартуем с первой страницы информации об авторах
    write_json('authors.json', authors_info)  # Сохраняем информацию об авторах в JSON