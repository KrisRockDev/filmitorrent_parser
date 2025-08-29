import os
import time
import shutil
import datetime
from icecream import ic
import requests
from settings import *
from bs4 import BeautifulSoup
from logger import print_error


def get_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP (например, 404, 500)
    except requests.RequestException as e:
        print_error(f"[get_info] Не удалось получить данные с {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим блок div с классом film-info
    film_info_div = soup.find("div", class_="film-info")

    if not film_info_div:
        print_error(f"[get_info] {url} Блок film-info не найден")
        return None

    rep_list = [
        ('Название:', '\n@Название:'),
        ('Оригинальное название:', '\n@Оригинальное название:'),
        ('Год:', '\n@Год:'),
        ('Продолжительность:', '\n@Продолжительность:'),
        ('Страна:', '\n@Страна:'),
        ('Рейтинг:', '\n@Рейтинг:'),
        ('Режиссер:', '\n@Режиссер:'),
        ('Актеры:', '\n@Актеры:'),
        ('Жанр:', '\n@Жанр:'),
        ('Опубликовано:', '\n@Опубликовано:'),
        ('Дата выхода в России:', '\n@Дата выхода в России:'),
        ('Премьера в мире:', '\n@Премьера в мире:'),
        (' , ', ', '),
        (': ', ':'),
        ('  ', ' '),
        (' \n', '\n'),
        ('\xa0', ''),
    ]

    # Извлекаем текст только из этого блока
    text = film_info_div.get_text(separator=" ", strip=True)

    for item in rep_list:
        text = text.replace(item[0], item[1])

    # Обрабатываем "Слоган" отдельно, так как он может отсутствовать
    text = text.replace('Слоган:', '\n@Слоган:').strip()
    text += f'\n@url:{url}'

    # --- СОЗДАНИЕ И СОХРАНЕНИЕ ФАЙЛА (без изменений) ---
    film_name = os.path.basename(url).split('.')[0]
    # Предполагается, что DOWNLOAD_DIR_ABSOLUTE определена в settings.py
    # film_dir = os.path.join(DOWNLOAD_DIR_ABSOLUTE, film_name)
    # os.makedirs(film_dir, exist_ok=True) # Создаем папку, если ее нет
    # file_path = os.path.join(film_dir, 'info.txt')

    # if not os.path.exists(file_path):
    #     with open(file=file_path, mode='w', encoding='utf-8') as f:
    #         f.write(text.replace('@', '')) # Сохраняем без @ для чистоты
    # else:
    #     pass

    # --- НОВАЯ ЧАСТЬ: СОЗДАНИЕ И ВОЗВРАТ СЛОВАРЯ ---
    info_dict = {
        'title': '',
        'original_title': '',
        'year': '',
        'duration': '',
        'country': '',
        'rating': '',
        'director': '',
        'actors': '',
        'genre': '',
        'published': '',
        'release_date_russia': '',
        'world_premiere': '',
        'slogan': '',

    }
    key_mapping = {
        '@Название': 'title',
        '@Оригинальное название': 'original_title',
        '@Год': 'year',
        '@Продолжительность': 'duration',
        '@Страна': 'country',
        '@Рейтинг': 'rating',
        '@Режиссер': 'director',
        '@Актеры': 'actors',
        '@Жанр': 'genre',
        '@Опубликовано': 'published',
        '@Дата выхода в России': 'release_date_russia',
        '@Премьера в мире': 'world_premiere',
        '@Слоган': 'slogan',
        # '@url': 'url'
    }

    lines = text.strip().split('\n')
    for line in lines:
        if ':' in line:
            # Разделяем строку только по первому вхождению ':'
            key_raw, value = line.split(':', 1)
            key_clean = key_raw.strip()

            # Находим соответствующий английский ключ
            if key_clean in key_mapping:
                english_key = key_mapping[key_clean]
                info_dict[english_key] = value.strip()

    return info_dict


if __name__ == '__main__':
    # Заглушки для запуска, если нет файлов settings.py и logger.py
    DOWNLOAD_DIR_ABSOLUTE = '.'


    def print_error(msg):
        print(f"ERROR: {msg}")


    url = 'https://filmitorrent.net/fantastika/5625-lilo-i-stich-2025.html'

    # Получаем словарь
    film_data = get_info(url)

    # Выводим результат
    if film_data:
        print("Словарь с данными о фильме:")
        # Используем ic для красивого вывода, если он установлен
        try:
            from icecream import ic

            ic(film_data)
        except ImportError:
            import pprint

            pprint.pprint(film_data)