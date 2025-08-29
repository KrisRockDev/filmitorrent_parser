import os
import time
import shutil
import datetime
import requests
from icecream import ic
from bs4 import BeautifulSoup
from settings import *
from logger import print_error


def get_poster(url, film_dir):
    try:
        # Выполняем запрос к странице
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Находим элемент <div class="poster-big">
        poster_div = soup.find("div", class_="poster-big")
        if poster_div:
            # Извлекаем тег <img> внутри <div>
            img_tag = poster_div.find("img")
            if img_tag and "src" in img_tag.attrs:
                # Получаем URL изображения
                img_url = img_tag["src"]

                # Преобразуем относительный путь в абсолютный
                if img_url.startswith("/"):
                    img_url_abs = FILMITORRENT_URL + img_url
                # film_dir = os.path.join(base_dir_absolute, os.path.basename(url).split('.')[0])

                # Имя файла для сохранения
                img_filename = os.path.join(film_dir, 'poster.' + os.path.basename(img_url).split('.')[-1])

                # ic(img_filename)
                # ic(img_url)
                # ic(img_url_abs)

                # Скачиваем изображение
                if not os.path.exists(img_filename):
                    img_response = requests.get(img_url_abs)
                    img_response.raise_for_status()  # Проверяем на ошибки HTTP

                    # Сохраняем изображение в файл
                    with open(img_filename, "wb") as file:
                        file.write(img_response.content)

                    # print(f"Изображение успешно скачано и сохранено как '{img_filename}'")
                else:
                    # print(f"Изображение уже сохранено как '{img_filename}'")
                    pass
            else:
                print_error(f"[get_image] {url} Изображение не найдено в теге <img>.")
        else:
            print_error(f"[get_image] {url} Элемент <div class='poster-big'> не найден.")
        return {'poster': img_url_abs}
    except requests.exceptions.RequestException as e:
        print_error(f"[get_image] {url} Ошибка при загрузке страницы или изображения: {e}")


if __name__ == '__main__':
    url = 'https://filmitorrent.net/fantastika/5625-lilo-i-stich-2025.html'
    film_dir = os.path.join(DOWNLOAD_DIR_ABSOLUTE, os.path.basename(url).split('.')[0])
    get_poster(url, film_dir)
