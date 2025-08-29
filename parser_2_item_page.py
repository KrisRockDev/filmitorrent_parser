import os

import requests
from bs4 import BeautifulSoup

from logger import print_error
from settings import *
from service_func import create_film_dir, save_html_page, get_datetime


def read_item_page(page_number):
    try:
        # Выполняем запрос к странице
        URL = f'{FILMITORRENT_URL}page/{page_number}/'
        response = requests.get(URL)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        html_content = response.text

        # Сохраняет HTML страницу для отладки
        # save_html_page(f'{get_datetime()}_page_{page_number}', html_content)

        soup = BeautifulSoup(html_content, "html.parser")  # Парсим HTML
        # Ищем родительский блок "post", а не "post-title" ---
        posts = soup.find_all("div", class_="post")

        # Сохраняем ссылки и текст
        results = []
        # Итерируемся по списку постов ---
        for post in reversed(posts):  # reversed() реверсирует список
            post_title = post.find("div", class_="post-title")
            if not post_title:
                continue

            link_tag = post_title.find("a")
            if link_tag:
                link = link_tag["href"]
                title = os.path.basename(link).split('.')[0]
                id = title.split('-')[0]
                text = link_tag.text.strip()
                category = link.split("/")[-2]

                # --- Поиск рейтинга внутри блока "post" ---
                kinopoisk_rating = '' # Значение по умолчанию
                rating_div = post.find("div", class_="frate-kp")
                if rating_div:
                    kinopoisk_rating = rating_div.text.strip()

                film_dict = {
                    "link": link,
                    "title_ru": text,
                    'item': title,
                    'category': category,
                    'id': id,
                    'kinopoisk': kinopoisk_rating # Добавляем новое поле в словарь
                }
                results.append(film_dict)

        return results

    except requests.exceptions.RequestException as e:
        print_error(f"[read_films_page] {FILMITORRENT_URL} Ошибка при загрузке страницы: {e}")
        return None


if __name__ == '__main__':
    page_number=str(1)
    results = read_item_page(page_number)
    print(results)


# import os
#
# import requests
# from bs4 import BeautifulSoup
#
# from logger import print_error
# from settings import *
# from service_func import create_film_dir, save_html_page, get_datetime
#
#
# def read_item_page(page_number):
#     try:
#         # Выполняем запрос к странице
#         URL = f'{FILMITORRENT_URL}page/{page_number}/'
#         response = requests.get(URL)
#         response.raise_for_status()  # Проверяем на ошибки HTTP
#         html_content = response.text
#
#         # Сохраняет HTML страницу для отладки
#         save_html_page(f'{get_datetime()}_page_{page_number}', html_content)
#
#         soup = BeautifulSoup(html_content, "html.parser")  # Парсим HTML
#         post_titles = soup.find_all("div", class_="post-title")  # Находим все элементы <div class="post-title">
#
#         # Сохраняем ссылки и текст
#         results = []
#         for post_title in reversed(post_titles):  # reversed() реверсирует список
#             link_tag = post_title.find("a")
#             if link_tag:
#                 link = link_tag["href"]
#                 title = os.path.basename(link).split('.')[0]
#                 id = title.split('-')[0]
#                 text = link_tag.text.strip()
#                 category = link.split("/")[-2]
#                 film_dict = {
#                     "link": link,
#                     "title_ru": text,
#                     'item': title,
#                     'category': category,
#                     'id': id,
#                 }
#                 results.append(film_dict)
#
#         return results
#
#     except requests.exceptions.RequestException as e:
#         print_error(f"[read_films_page] {FILMITORRENT_URL} Ошибка при загрузке страницы: {e}")
#         return None
#
#
# if __name__ == '__main__':
#     page_number=str(1)
#     results = read_item_page(page_number)
#     print(results)
#
#
#
# import os
#
# import requests
# from bs4 import BeautifulSoup
#
# # Заглушки для ваших импортированных функций, чтобы скрипт был рабочим
# def print_error(message):
#     print(message)
#
# def save_html_page(filename, content):
#     # с pathlib это будет безопаснее для разных ОС
#     from pathlib import Path
#     debug_dir = Path("debug_pages")
#     debug_dir.mkdir(exist_ok=True)
#     (debug_dir / f"{filename}.html").write_text(content, encoding='utf-8')
#
#
# def get_datetime():
#     from datetime import datetime
#     return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#
# # Заглушка для ваших настроек
# FILMITORRENT_URL = "https://filmitorrent.net/"
# # --- Конец заглушек ---
#
#
# def read_item_page(page_number):
#     try:
#         # Выполняем запрос к странице
#         URL = f'{FILMITORRENT_URL}page/{page_number}/'
#         response = requests.get(URL)
#         response.raise_for_status()  # Проверяем на ошибки HTTP
#         html_content = response.text
#
#         # Сохраняет HTML страницу для отладки
#         save_html_page(f'{get_datetime()}_page_{page_number}', html_content)
#
#         soup = BeautifulSoup(html_content, "html.parser")
#         # Находим все родительские блоки <div class="post">
#         posts = soup.find_all("div", class_="post")
#
#         # Сохраняем результаты
#         results = []
#         # reversed() реверсирует список для обработки от старых постов к новым
#         for post in reversed(posts):
#             post_title = post.find("div", class_="post-title")
#             if not post_title:
#                 continue # Пропускаем, если у поста нет заголовка
#
#             link_tag = post_title.find("a")
#             if link_tag:
#                 link = link_tag["href"]
#                 title = os.path.basename(link).split('.')[0]
#                 id_film = title.split('-')[0]
#                 text = link_tag.text.strip()
#                 category = link.split("/")[-2]
#
#                 # Ищем рейтинг Кинопоиска
#                 kinopoisk_rating = None
#                 rating_div = post.find("div", class_="frate-kp")
#                 if rating_div:
#                     kinopoisk_rating = rating_div.text.strip()
#
#                 film_dict = {
#                     "link": link,
#                     "title_ru": text,
#                     'item': title,
#                     'category': category,
#                     'id': id_film,
#                     'kinopoisk': kinopoisk_rating # Добавляем рейтинг в словарь
#                 }
#                 results.append(film_dict)
#
#         return results
#
#     except requests.exceptions.RequestException as e:
#         print_error(f"[read_item_page] {FILMITORRENT_URL} Ошибка при загрузке страницы: {e}")
#         return None
#
#
# if __name__ == '__main__':
#     page_number = str(1)
#     results = read_item_page(page_number)
#     # Выводим результаты в более читаемом виде
#     if results:
#         for item in results:
#             print(item)