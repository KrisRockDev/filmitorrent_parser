import os
import shutil
import datetime
from settings import *


def create_dir(dir):
    if dir not in os.listdir():
        os.makedirs(dir, exist_ok=True)


for i in list_dir:
    if not os.path.exists(i):
        create_dir(i)


def del_dir():
    lst = os.listdir(DOWNLOAD_DIR)
    if len(lst) > LIMIT:
        del_list = lst[:-1 * LIMIT]
        for item in del_list:
            folder_path = os.path.join(DOWNLOAD_DIR, item)  # удаление папки
            # Проверяем, существует ли папка
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                # Удаляем папку и все её содержимое
                shutil.rmtree(folder_path)


def create_film_dir(title):
    create_dir(DOWNLOAD_DIR)
    if title not in os.listdir(DOWNLOAD_DIR):
        os.mkdir(os.path.join(DOWNLOAD_DIR, title))
    # print(f"{title=}")
    del_dir()
    return title


def save_html_page(file_name, html_content):
    file_path = os.path.join(HTML_DIR_ABSOLUTE, file_name)
    create_dir(HTML_DIR_ABSOLUTE)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✔️ HTML-страница успешно сохранена в файл: '{file_name}'")


def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")
