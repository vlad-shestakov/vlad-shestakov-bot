import params as p # Параметры приложения
import requests
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

# Токен телеграм бота
# Путь до API Homelib
if p.STAND_TYPE == p.STAND_TYPE_PROD:
    API_HOMEPATH = os.getenv("API_HOMEPATH")
else:
    API_HOMEPATH = os.getenv("API_HOMEPATH_TEST")

print(f"API_HOMEPATH - {API_HOMEPATH}")

BOOK_LIST_PAGE_CNT      = int(os.getenv("BOOK_LIST_PAGE_CNT", 40))    # Количество книг на странице списка книг
# Сортировка полей в списках
BOOK_LIST_SORT          = 'createdAt,desc&sort=author&sort=title'       # Список книг
CATS_LIST_SORT          = 'published,desc&sort=author&sort=title'       # Каталог книг

HOMELIB_MAIN_IMAGE      = 'homelib_cover.jpg'
HOMELIB_MAIN_COMMAND    = 'homelib'
LIST_BOOKS_COMMAND      = 'books'
LAST_BOOKS_COMMAND      = 'recentbooks'
CATS_BOOKS_COMMAND      = 'categories'
SEARCH_BOOKS_COMMAND    = 'booksrch'

OBJ_BOOK_COMMAND        = '/b'
OBJ_LIB_PAGE_COMMAND    = '/p'
OBJ_CAT_PAGE_COMMAND    = '/cat_'

MIN_SYMBOLS_SEARCH      = 3 # Минимальное количество символов поиска

ERR_MSG_SERVICE_NOT_AVAILABLE           = 'Сервис недоступен. Обратитесь к администратору.'

ERR_MSG_SERVICE_BOOKS_LIST_EMPTY        = ERR_MSG_SERVICE_NOT_AVAILABLE
ERR_MSG_SERVICE_BOOKS_BY_CAT_LIST_EMPTY = ERR_MSG_SERVICE_NOT_AVAILABLE
ERR_MSG_SERVICE_CATS_LIST_EMPTY         = ERR_MSG_SERVICE_NOT_AVAILABLE
ERR_MSG_SERVICE_BOOK_EMPTY              = ERR_MSG_SERVICE_NOT_AVAILABLE

# Ассоциации категорий с алиасами
categories_map = [
 	{"cat_alias": "bio", "category": "Biography"},
    {"cat_alias": "bio_bzn_ecn", "category": "Biography, Business & Economics"},
    {"cat_alias": "bio_nonf", "category": "Biography, Non Fiction"},
    {"cat_alias": "bio_arts", "category": "Biography, Performing Arts"},
    {"cat_alias": "bzn_ecn", "category": "Business & Economics"},
    {"cat_alias": "baz_ecn_comp", "category": "Business & Economics, Computers"},
    {"cat_alias": "bzn_ecn_plt", "category": "Business & Economics, Political Science"},
    {"cat_alias": "comp", "category": "Computers"},
    {"cat_alias": "fict", "category": "Fiction"},
    {"cat_alias": "hlt_med", "category": "Health, Medicine, Body"},
    {"cat_alias": "history", "category": "History"},
    {"cat_alias": "hobby_food", "category": "Hobbies, Food"},
    {"cat_alias": "nonf", "category": "Non Fiction"},
    {"cat_alias": "nonf_comp", "category": "Non Fiction, Computers"},
    {"cat_alias": "nonf_hobby_food", "category": "Non Fiction, Hobbies, Food"},
    {"cat_alias": "nonf_arts", "category": "Non Fiction, Performing Arts"},
    {"cat_alias": "nonf_plt", "category": "Non Fiction, Political Science"},
    {"cat_alias": "nonf_psy", "category": "Non Fiction, Psychology"},
    {"cat_alias": "arts", "category": "Performing Arts"},
    {"cat_alias": "pol", "category": "Political Science"},
    {"cat_alias": "psy", "category": "Psychology"},
    # {"cat_alias": "religion", "category": "Religion"},
    {"cat_alias": "tourism", "category": "Tourism"}
]

# ----------------------------------------------------------
def find_category_by_cat_alias(cat_alias):
    # Находит category по полю cat_alias
    for item in categories_map:
        if item["cat_alias"] == cat_alias:
            return item["category"]
    return None

# ----------------------------------------------------------
def find_cat_alias_by_category(category):
    # Находит cat_alias по полю category
    for item in categories_map:
        if item["category"] == category:
            return item["cat_alias"]
    return None

# ----------------------------------------------------------
def fetch_all_books(page = 0) -> List[Dict]:
    # Получает данные о списке книг с API и типизирует их в список словарей.
    url = f'{API_HOMEPATH}/books?page={page}&size={BOOK_LIST_PAGE_CNT}&sort={BOOK_LIST_SORT}'
    if p.IS_DEBUG:
        print(f'url - {url}')
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    books: List[Dict] = response.json()
    return books

# ----------------------------------------------------------
def fetch_recent_books() -> List[Dict]:
    # Получает данные о списке последних книг с API и типизирует их в список словарей
    url = f'{API_HOMEPATH}/books?recent'
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    books: List[Dict] = response.json()
    return books

# ----------------------------------------------------------
def fetch_books_by_cat(cat_alias = None) -> List[Dict]:
    # Получает данные о списке книг по категории с API и типизирует их в список словарей.
    category = find_category_by_cat_alias(cat_alias)
    # Если по алиасу не нашлась строка поиска, поищем по тексту алиаса
    if category is not None:
        url = f'{API_HOMEPATH}/books?category={category}&sort={CATS_LIST_SORT}'
    else:
        url = f'{API_HOMEPATH}/books?category={cat_alias}&sort={CATS_LIST_SORT}'
    if p.IS_DEBUG:
        print(f'url - {url}')
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    books: List[Dict] = response.json()
    return books

# ----------------------------------------------------------
def fetch_search_books_by_title_autor(search_text) -> List[Dict]:
    # Ищет книги по строке поиска в названии, авторе из API и типизирует их в список словарей.
    url = f'{API_HOMEPATH}/books/search?searchText={search_text}'
    if p.IS_DEBUG:
        print(f'url - {url}')
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    books: List[Dict] = response.json()
    return books

# ----------------------------------------------------------
def fetch_categories() -> List[Dict]:
    # Получает данные о списке категорий книг с API и типизирует их в список словарей.
    url = f'{API_HOMEPATH}/books/categories'
    if p.IS_DEBUG:
        print(f'url - {url}')
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    cats: List[Dict] = response.json()
    return cats

# ----------------------------------------------------------
def get_books(page = 0):
    # Возвращает список книг
    res = {}
    currentPage = {}
    totalPages = {}
    try:
        books_data = fetch_all_books(page)
        res = books_data['content']
        # res = books_data['_embedded']['books']
        currentPage = books_data['pageable']['pageNumber']
        # currentPage = books_data['page']['number']
        totalPages = books_data['totalPages']
        # totalPages = books_data['page']['totalPages']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res, currentPage, totalPages

# ----------------------------------------------------------
def get_recent_books():
    # Возвращает список книг
    res = {}
    try:
        books_data = fetch_recent_books()
        res = books_data
        # res = books_data['_embedded']['books']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res

# ----------------------------------------------------------
def get_books_by_cat(cat_alias = None):
    # Возвращает список книг по категории
    res = {}
    try:
        books_data = fetch_books_by_cat(cat_alias)
        res = books_data['content']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res

# ----------------------------------------------------------
def get_search_books_by_title_autor(search_text):
    # Возвращает книги по строке поиска в названии
    res = {}
    try:
        books_data = fetch_search_books_by_title_autor(search_text)
        res = books_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res

# ----------------------------------------------------------
def get_categories():
    # Возвращает список категорий книг
    res = {}
    try:
        res = fetch_categories()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res

# ----------------------------------------------------------
def get_book_name(book_obj):
    # Возвращает название книги
    # * [Год. ][Автор - ]НазваниеКниги
    msg = None
    try:
        published = book_obj.get('published', '')
        author = book_obj.get('author', '')
        title = book_obj.get('title', '')
        year_text = ''
        if published is not None and published != '':
            year_text = f'{published}. '
        author_text = ''
        if author is not None and author != '':
            author_text = f'{author} - '
        msg = f"{year_text}{author_text}{title}"
    except:
        None
    return msg

# ----------------------------------------------------------
def get_books_list_block_text(books_obj):
    # Возвращает текст списка книг
    msg = ''
    for i, book_obj in enumerate(books_obj):
        try:
            # Формируем строку
            # * [Год. ][Автор - ]НазваниеКниги[(/bНомерКниги)]
            book_name = get_book_name(book_obj)
            try:
                book_id = int(book_obj['id'])
                # достаем 456 из объекта - "_links": {"self": {"href": "http://some_url/books/456"
                # book_id = int(book_obj['_links']['self']['href'].rsplit('/', 1)[-1])
                book_link = f' ({OBJ_BOOK_COMMAND}{book_id})' #/b123456
            except:
                book_link = ''
            msg = msg + f"\n * {book_name}{book_link}"
        except:
            None
    return msg

# ----------------------------------------------------------
def get_books_list_text(books_obj, currentPage, totalPages):
    # Возвращает текст списка книг
    msg = f"Список книг: (Страница {currentPage + 1} из {totalPages})\n"
    # Добавляем список книг из объекта
    msg = msg + get_books_list_block_text(books_obj)
    if totalPages > 1:
        msg = msg + "\n"
    if currentPage > 0:
        prevPage = currentPage # не вычитаем, т.к. нужно преобразование не нулевой а первой страницы
        msg = msg + f"\n<<< Страница {OBJ_LIB_PAGE_COMMAND}{prevPage}"
    if currentPage + 1 < totalPages:
        nextPage = currentPage + 2 # добавляем 2, т.к. нужно преобразование не нулевой а первой страницы
        msg = msg + f"\nСтраница >>> {OBJ_LIB_PAGE_COMMAND}{nextPage}"
    msg = msg + f"\nГлавная страница /{HOMELIB_MAIN_COMMAND}"
    return msg

# ----------------------------------------------------------
def get_recent_books_list_text(books_obj):
    # Возвращает текст списка книг
    msg = f"Последние поступления:\n"
    # Добавляем список книг из объекта
    msg = msg + get_books_list_block_text(books_obj)
    msg = msg + f"\n\nГлавная страница /{HOMELIB_MAIN_COMMAND}"
    return msg

# ----------------------------------------------------------
def get_books_by_cat_list_text(books_obj, cat_alias = None):
    # Возвращает текст списка книг
    category = find_category_by_cat_alias(cat_alias)
    # Если по алиасу не нашлась категория, выведем алиас
    if category is None:
        category = cat_alias
    msg = f"Книги. Категория - {category}:\n"
    # Добавляем список книг из объекта
    msg = msg + get_books_list_block_text(books_obj) \
             + f"\n\nСписок категорий /{CATS_BOOKS_COMMAND}" \
             + f"\nГлавная страница /{HOMELIB_MAIN_COMMAND}"
    return msg

# ----------------------------------------------------------
def get_search_books_by_title_autor_text(books_obj, search_text):
    # Возвращает список книг в результате поиска
    msg = f"Поиск по названию, автору: {search_text}\n"
    # Добавляем список книг из объекта
    msg = msg + get_books_list_block_text(books_obj) \
             + f"\n\nДругой поиск /{SEARCH_BOOKS_COMMAND}" \
             + f"\nГлавная страница /{HOMELIB_MAIN_COMMAND}"
    return msg

# ----------------------------------------------------------
def get_cat_link_text(category):
    # Возвращает текст ссылки на категорию книг вида /cat_ALIAS
    res = None
    cat_alias = find_cat_alias_by_category(category)
    if cat_alias is not None and len(cat_alias) > 0:
        res = f"{OBJ_CAT_PAGE_COMMAND}{cat_alias}"
    elif category is not None and len(category) > 0:
        res = f"{OBJ_CAT_PAGE_COMMAND}{category}"
    return res

# ----------------------------------------------------------
def get_cats_list_text(cats_obj):
    # '/categories' - Возвращает список категорий книг библиотеки для телеграма
    # Возвращает текст список категорий книг
    msg = f"Список категорий:\n"
    for i, cat_obj in enumerate(cats_obj):
        try:
            # Формируем строку
            category = str(cat_obj)
            cat_link_text = get_cat_link_text(category)
            msg = msg + f"\n * {category}"
            if cat_link_text is not None:
                msg = msg + f" ({cat_link_text})"
        except:
            None
    msg = msg + f"\n\nГлавная страница /{HOMELIB_MAIN_COMMAND}"
    return msg

# ----------------------------------------------------------
# '/books' - Возвращает текст списка книг библиотеки для телеграма
def get_msg_books_list(page = 0):
    books_dict, currentPage, totalPages = get_books(page)
    if books_dict is None or len(books_dict) == 0:
        msg = ERR_MSG_SERVICE_BOOKS_LIST_EMPTY
    else:
        msg = get_books_list_text(books_dict, currentPage, totalPages)
    return msg

# ----------------------------------------------------------
# '/cat_NNN' - Возвращает текст списка книг библиотеки по категории для телеграма
def get_msg_books_by_cat_list(cat_alias = None):
    books_dict = get_books_by_cat(cat_alias)
    if books_dict is None or len(books_dict) == 0:
        msg = ERR_MSG_SERVICE_BOOKS_BY_CAT_LIST_EMPTY
    else:
        msg = get_books_by_cat_list_text(books_dict, cat_alias)
    return msg

# ----------------------------------------------------------
# '/booksrch' - Возвращает текст списка книг при поиске по названию, автору
def get_msg_search_books_by_title_autor(search_text):
    books_dict = get_search_books_by_title_autor(search_text)
    if books_dict is None or len(books_dict) == 0:
        msg = f"Ничего не нашлось" + \
            f"\n\nПопробуйте поискать снова /{SEARCH_BOOKS_COMMAND}"
    else:
        msg = get_search_books_by_title_autor_text(books_dict, search_text)
    return msg

# ----------------------------------------------------------
# '/categories' - Возвращает список категорий книг библиотеки для телеграма
def get_msg_cats_list():
    cats_dict = get_categories()
    # print(f'cats_dict - {cats_dict}')
    if cats_dict is None or len(cats_dict) == 0:
        msg = ERR_MSG_SERVICE_CATS_LIST_EMPTY
    else:
        msg = get_cats_list_text(cats_dict)
    return msg

# ----------------------------------------------------------
def fetch_book(book_id) -> List[Dict]:
    # Получает данные о книге с API и типизирует их в список словарей.
    url = f'{API_HOMEPATH}/books/{book_id}'
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    book_dict: List[Dict] = response.json()
    return book_dict


# ----------------------------------------------------------
def fetch_book_cover(book_id):
    img_data = None
    try:
        # Получает фото обложки книги
        url = f'{API_HOMEPATH}/books/cover/{book_id}'

        # Проверяем доступность изображения по URL
        response = requests.get(url)
        if response.status_code != 200 or not response.content:
            raise ValueError('Картинка не доступна.')

        # Преобразуем полученный контент в файл для отправки
        img_data = BytesIO(response.content)
        img_data.seek(0)

        return img_data

    except Exception as e:
        # bot.reply_to(message, f"Произошла ошибка: {e}")
        return img_data

# ----------------------------------------------------------
def get_book(book_id):
    # Возвращает данные книги по номеру
    res = None
    try:
        book_data = fetch_book(book_id)
        res = book_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res


# ----------------------------------------------------------
def get_book_cover(book_id):
    # Возвращает данные книги по номеру
    res = None
    try:
        img_data = fetch_book_cover(book_id)
        res = img_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    return res

# ----------------------------------------------------------
def get_date_str(timestamp):
    # Преобразование объекта timestamp '2024-09-30T21:00:00.000+00:00' в строку 30.09.2024
    try:
        # Преобразование строки в объект datetime
        dt_object = datetime.fromisoformat(str(timestamp))
        # Форматирование даты в нужный вид
        res = dt_object.strftime('%d.%m.%Y')
    except:
        res = ""
    return res

# ----------------------------------------------------------
def get_attr(attr_data):
    # Безопасное получение атрибута
    res = ''
    try:
        if attr_data is not None and len(attr_data) > 0:
            res = attr_data
    except:
        None
    return res

# ----------------------------------------------------------
def get_format_attr(attr_data, attr_text):
    # условное добавление атрибута - [\nATTR_TEXT: ATTR_NAME]
    res = ''
    try:
        # print(f'attr_data - {attr_data}, attr_text - {attr_text}')
        # print(f'len(attr_data) - {len(attr_data)}')
        if attr_data is not None and len(attr_data) > 0:
            res = f'\n{attr_text}: {attr_data}'
    except:
        attr_data = ''
        attr_text = ''
    return res

# ----------------------------------------------------------
def check_file_link(coverUrl):
    # условное добавление атрибута - [\nATTR_TEXT: ATTR_NAME]
    return coverUrl if coverUrl.startswith('http') else None

# ----------------------------------------------------------
def get_book_text(book_obj):
    # Возвращает текст карточки книги

    # [Год. ][Автор - ]НазваниеКниги
    #
    # Издательство: Медиарост
    # Категория: History (/cat_NNN)
    # Серия: Жизнь замечательных людей
    # Ссылка: https://www.livelib.ru/book/1009317952-rossiya-vek-xx-19011964-opyt-bespristrastnogo-issledovaniya-vadim-kozhinov
    # Страница автора: https://www.livelib.ru/author/214708
    # ISBN: 9785045469715
    # Обложка: https://books.google.com/books/content?id=KLm9EAAAQBAJ&printsec=frontcover&img=1&source=gbs_api
    # Добавлено: 11.03.2025

    book_name   = ''
    pubName     = ''
    category    = ''
    serieName   = ''
    bookLink    = ''
    authorLink  = ''
    isbn        = ''
    coverUrl    = ''
    createdAt   = ''
    
    book_name = get_book_name(book_obj) # Название книги - [Год. ][Автор - ]НазваниеКниги
    pubName = get_format_attr(book_obj['pubName'], 'Издательство')
    category = get_format_attr(book_obj['category'], 'Категория')
    cat_link_text = get_cat_link_text(get_attr(book_obj['category']))
    if cat_link_text is not None:
        category = category + f" ({cat_link_text})"
    serieName = get_format_attr(book_obj['serieName'], 'Серия')
    bookLink = get_format_attr(book_obj['bookLink'], 'Ссылка')
    authorLink = get_format_attr(book_obj['authorLink'], 'Страница автора')
    try:
        isbn_obj = (book_obj['isbn'])
        isbn = get_format_attr(isbn_obj, 'ISBN')
    except:
        None
    try:
        coverUrl_obj = book_obj['coverUrl']
        coverUrl = get_format_attr(check_file_link(coverUrl_obj), 'Обложка')
    except:
        None
    createdAt = get_format_attr(get_date_str(book_obj['createdAt']), 'Добавлено')
    try:
        msg = f'{book_name}\n{pubName}{category}{serieName}{bookLink}{authorLink}{isbn}{coverUrl}{createdAt}'
    except:
        None
    return msg

# ----------------------------------------------------------
# Получаем book_id из ссылки
def check_command_book_id(command_text):
    book_id = None
    try:
        if command_text.startswith(OBJ_BOOK_COMMAND):
            book_id = int(command_text.split(OBJ_BOOK_COMMAND)[1])
    except:
        None
    return book_id

# ----------------------------------------------------------
# Получаем cat_name из ссылки
def check_command_cat_name(command_text):
    cat_name = None
    try:
        if command_text.startswith(OBJ_CAT_PAGE_COMMAND):
            cat_name = command_text.split(OBJ_CAT_PAGE_COMMAND)[1]
    except:
        None
    return cat_name

# ----------------------------------------------------------
# Получаем page_id из ссылки
def check_command_lib_page_id(command_text):
    page_id = -1
    try:
        if command_text.startswith(OBJ_LIB_PAGE_COMMAND):
            page_id = int(command_text.split(OBJ_LIB_PAGE_COMMAND)[1]) - 1
    except:
        None
    return page_id

# ----------------------------------------------------------
# Возвращает текст карточки книги для ТГ бота
def get_msg_book_by_id(book_id):
    # print(f'get_msg_book_by_id({book_id})')
    # Вывод
    # * msg         - информации об одной книге
    # * img_cover   - обложке книги
    book_obj = get_book(book_id)
    img_cover = get_book_cover(book_id)
    if book_obj is None or len(book_obj) == 0:
        msg = ERR_MSG_SERVICE_BOOK_EMPTY
    else:
        msg = get_book_text(book_obj)
    return msg, img_cover


# ----------------------------------------------------------
# Возвращает текст Главной страницы библиотеки
def get_msg_homelib_main():
    msg = f"""Домашняя библиотека

Список книг /{LIST_BOOKS_COMMAND}
Список категорий /{CATS_BOOKS_COMMAND}
Последние поступления /{LAST_BOOKS_COMMAND}
Поиск по названию, автору /{SEARCH_BOOKS_COMMAND}
"""
    return msg

# ----------------------------------------------------------
# '/recentbooks' - Возвращает текст Cтраницы Последние поступления
def get_msg_books_recent_list():
    books_dict = get_recent_books()
    if books_dict is None or len(books_dict) == 0:
        msg = ERR_MSG_SERVICE_BOOKS_LIST_EMPTY
    else:
        msg = get_recent_books_list_text(books_dict)
    return msg


# ----------------------------------------------------------
# Проверяет текст сообщения для поиска по названию, автору
# Возвращает
#  res      - Код ошибки 0/1
#  err_msg  - Текст ошибки
def check_msg_homelib_booksearch(search_text):
    res = 0
    err_msg = None
    if search_text is None or len(search_text) < MIN_SYMBOLS_SEARCH:  # Минимальное количество символов поиска
        err_msg = f"Минимальная длина строки поиска должна составлять {MIN_SYMBOLS_SEARCH} символа."
        err_msg = err_msg + f"\n\nПопробуйте поискать снова /{SEARCH_BOOKS_COMMAND}"
        res = 1
    return res, err_msg

# ----------------------------------------------------------
# Возвращает текст сообщения - поиск по названию, автору
def get_msg_homelib_booksearch():
    return "Введите строку поиска по названию, автору:"