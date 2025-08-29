import os

# Сайт с новинками кино
FILMITORRENT_URL = 'http://filmitorrent.net/'

# файл со списком фильмов, для исключения отправки повторного уведомления
films_list_base = 'films_list.txt'

# файл для добавления новых пользователей (CHAT_ID)
users_file = 'users.txt'


# директория для скачивания
DOWNLOAD_DIR = 'downloads'
DOWNLOAD_DIR_ABSOLUTE = os.path.abspath(DOWNLOAD_DIR)

# директория с пользователями
USERS_DIR = 'users'
USERS_DIR_ABSOLUTE = os.path.abspath(USERS_DIR)

# директория для логов
LOG_DIR = 'logs'
LOGS_DIR_ABSOLUTE = os.path.abspath(LOG_DIR)

# директория с пользователями
HTML_DIR = 'html_pages'
HTML_DIR_ABSOLUTE = os.path.abspath(HTML_DIR)

list_dir = [
    DOWNLOAD_DIR_ABSOLUTE,
    USERS_DIR_ABSOLUTE,
    LOGS_DIR_ABSOLUTE,
    HTML_DIR_ABSOLUTE,
]

# Количество фильмов сохраняем в папке base_dir (не рекомендуется менее 10 и более 100)
LIMIT = 10

# Переменная для режима отладки
# True - запуск бота в режиме отладки для однократного запуска
# False - запуск бота в режиме реальной работы для периодического парсинга сайта
# DEBUG = False
DEBUG = True

# ID канала для отправки сообщений
CHANNEL_ID = os.getenv("CHANNEL_ID")

# файл для хранения информации об отправленных сообщениях
POSTED_MESSAGES_DB = 'posted_messages.json'
