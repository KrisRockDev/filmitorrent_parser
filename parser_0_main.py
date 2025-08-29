import os
import time
from icecream import ic
from dotenv import load_dotenv

from logger import print_error
from service_func import *
from json_lib import *
from parser_1_max_pages import get_max_page_number  # находим максимальную страницу в пагинации
from parser_2_item_page import read_item_page  # возвращает список со ссылками на страницы фильмов
from parser_3_img import get_img
from parser_4_poster import get_poster
from parser_5_info import get_info
from parser_6_des import get_des
from parser_7_torrents import get_torrents
from settings import films_list_base

# Загрузить переменные окружения из .env
load_dotenv()


def main():
    # находим максимальную страницу в пагинации
    number_pages = get_max_page_number()
    start_page = 1
    count = 1 + (start_page-1)*10
    if number_pages:
        # for page in range(start_page, number_pages+1):
        for page in range(1, 4):
            print('--- Страница', page, '---')
            # возвращает список со ссылками на страницы фильмов
            films_list = read_item_page(str(page))
            for film_dict in films_list[::-1]:
                try:
                    url = film_dict['link']
                    print(f"{round(count/number_pages*10, 2)}% ", f'{count} {film_dict['title_ru']}', end='')

                    # Создаём директорию для загрузки файлов
                    film_dir = os.path.join(DOWNLOAD_DIR_ABSOLUTE, film_dict['item'])
                    create_dir(film_dir)

                    # Загрузка кадров из фильма
                    img_dict = get_img(url, film_dir)
                    film_dict = film_dict | img_dict
                    json_write(film_dict, os.path.join(film_dir, 'info.json'))
                    # print(f'- Кадры загружены')

                    # Загрузка постера фильма
                    poster_dict = get_poster(url, film_dir)
                    film_dict = film_dict | poster_dict
                    json_write(film_dict, os.path.join(film_dir, 'info.json'))
                    # print(f'- Постер загружен')

                    # Загрузка информации из фильма
                    info_dict = get_info(url)
                    film_dict = film_dict | info_dict
                    json_write(film_dict, os.path.join(film_dir, 'info.json'))
                    # print(f'- Информация загружена')

                    # Загрузка описания фильма
                    des_dict = get_des(url)
                    film_dict = film_dict | des_dict
                    json_write(film_dict, os.path.join(film_dir, 'info.json'))
                    # print(f'- Описание загружено')

                    torrent_dict = get_torrents(url, film_dir)
                    film_dict = film_dict | {'torrents': torrent_dict}
                    # print(f'- Файлы торрент загружены')

                    json_write(film_dict, os.path.join(film_dir, 'info.json'))

                    count += 1
                    print(f" ✅")

                except Exception as e:
                    count += 1
                    print(f" ❌")
                    print_error(f"[main] {url} Ошибка при загрузке страницы: {e}")


if __name__ == '__main__':
    print('Загружаю фильмы')
    main()
