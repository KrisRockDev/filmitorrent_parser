import dropbox
import os
import datetime
from dotenv import load_dotenv

# --- ШАГ 1: НАСТРОЙКА И ПОДКЛЮЧЕНИЕ ---
def dropbox_connect():
    # Загружаем переменные окружения из файла .env
    load_dotenv()
    TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

    if not TOKEN:
        raise ValueError("Не удалось найти переменную DROPBOX_ACCESS_TOKEN. Проверьте ваш .env файл.")

    # Инициализируем клиент Dropbox и сразу проверяем подключение
    try:
        dbx = dropbox.Dropbox(TOKEN)
        dbx.users_get_current_account()
        print("✅ Успешное подключение к Dropbox!")
        return dbx
    except dropbox.exceptions.AuthError:
        print("❌ ОШИБКА: Неверный токен доступа. Проверьте токен и права доступа у приложения в Dropbox.")
        exit()

# --- ШАГ 2: ОБНОВЛЕННЫЕ И НАДЕЖНЫЕ ФУНКЦИИ ---

def upload_file(local_file_path, remote_folder_path, now=False):
    """
    Загружает локальный файл в указанную папку на Dropbox.
    Если файл с таким именем уже существует, он будет перезаписан.
    local_file_path - полный путь до локального файла на устройсте.
    remote_folder_path - папка в которую записываем файл на Dropbox.
    now - добавление метки времени к началу названия файла
        по умолчанию имеет значение False
    """
    # Проверяем подключение к dropbox
    dbx = dropbox_connect()

    if now:
        now = f'{get_datetime()}_'
    else:
        now = ''

    # Формируем полный путь к файлу на сервере, используя только прямые слэши
    remote_file_path = f"{remote_folder_path}/{now}{os.path.basename(local_file_path)}"

    # print(f"\n--- UPLOAD/UPDATE: Загрузка '{local_file_path}' в '{remote_file_path}' ---")
    try:
        # Открываем локальный файл в бинарном режиме для чтения ('rb')
        with open(local_file_path, 'rb') as f:
            # Вызываем метод API для загрузки. mode='overwrite' отвечает за обновление.
            metadata = dbx.files_upload(f.read(), remote_file_path, mode=dropbox.files.WriteMode('overwrite'))
            print(f"✔️ Файл '{metadata.name}' успешно загружен/обновлен.")
    except FileNotFoundError:
        print(f"❌ ОШИБКА: Локальный файл не найден по пути '{local_file_path}'")
    except dropbox.exceptions.ApiError as err:
        print(f"❌ Ошибка API при загрузке файла: {err}")


def download_file(remote_file_path, local_destination_path):
    """Скачивает файл с Dropbox по указанному пути."""
    # Проверяем подключение к dropbox
    dbx = dropbox_connect()
    # print(f"\n--- DOWNLOAD: Скачивание '{remote_file_path}' в '{local_destination_path}' ---")
    try:
        metadata, res = dbx.files_download(path=remote_file_path)

        # Убедимся, что директория для сохранения файла существует
        directory = os.path.dirname(local_destination_path)
        if directory:  # Создаем директорию, только если путь к ней не пустой
            os.makedirs(directory, exist_ok=True)

        # Открываем локальный файл в бинарном режиме для записи ('wb')
        with open(local_destination_path, 'wb') as f:
            f.write(res.content)
        # print(f"✔️ Файл успешно скачан и сохранен как '{local_destination_path}'")
    except dropbox.exceptions.ApiError as err:
        if 'path/not_found' in str(err):
            print(f"❌ Ошибка: Файл не найден на сервере по пути '{remote_file_path}'")
        else:
            print(f"❌ Ошибка API при скачивании файла: {err}")


def delete_file(remote_file_path):
    """Удаляет файл или папку в Dropbox по указанному пути."""
    print(f"\n--- DELETE: Удаление объекта '{remote_file_path}' ---")
    try:
        metadata = dbx.files_delete_v2(remote_file_path)
        print(f"✔️ Объект '{metadata.name}' успешно удален с сервера.")
    except dropbox.exceptions.ApiError as err:
        if 'path_lookup/not_found' in str(err):
            print(f"❌ Ошибка: Объект не найден на сервере и не может быть удален.")
        else:
            print(f"❌ Ошибка API при удалении: {err}")


def list_folder(remote_folder_path):
    """Выводит содержимое папки на Dropbox."""
    # Проверяем подключение к dropbox
    dbx = dropbox_connect()
    # print(f"\nСодержимое папки на сервере '{remote_folder_path}':")
    try:
        result = dbx.files_list_folder(remote_folder_path)
        if not result.entries:
            print("(пусто)")
        files_list=[]
        folders_list=[]
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                entry_type = 'папка'
                folders_list.append(entry.name)
            else:
                entry_type = 'файл'
                files_list.append(entry.name)
            # print(f"- {entry.name} ({entry_type})")

        return folders_list, files_list
    except dropbox.exceptions.ApiError as err:
        if 'path/not_found' in str(err):
            print("(папка не найдена)")
        else:
            print(f"❌ Ошибка при получении списка файлов: {err}")
        return False  # Возвращаем неудачу


def cleanup_local_files(files_to_delete):
    """Удаляет список локальных файлов, созданных во время работы скрипта."""
    print("\n--- CLEANUP: Очистка временных локальных файлов ---")
    if not isinstance(files_to_delete, list):
        files_to_delete = [files_to_delete]  # Позволяет передавать и одну строку

    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✔️ Локальный файл '{file_path}' удален.")
            except OSError as e:
                print(f"❌ Не удалось удалить локальный файл '{file_path}': {e}")
        else:
            print(f"ℹ️ Локальный файл '{file_path}' для очистки не найден, пропуск.")


# --- ШАГ 3: ДЕМОНСТРАЦИЯ РАБОТЫ СКРИПТА ---

# Этот блок будет выполнен только при запуске файла напрямую
if __name__ == "__main__":
    # --- 1. ОПРЕДЕЛЯЕМ ПУТИ И ДАННЫЕ ---
    # Путь к папке на Dropbox, где будет происходить вся работа
    REMOTE_WORK_FOLDER = '/data/test_folder'

    # Локальные файлы для демонстрации
    LOCAL_ORIGINAL_FILE = 'README.md'
    LOCAL_UPDATED_FILE = 'updated.txt'
    LOCAL_DOWNLOADED_FILE = '20250814_095346_README.md'

    # Полный путь к файлу на сервере (формируется автоматически)
    REMOTE_FILE_PATH = f"{REMOTE_WORK_FOLDER}/{os.path.basename(LOCAL_ORIGINAL_FILE)}"
    DOWNLOADED_FILE_PATH = f"{REMOTE_WORK_FOLDER}/{os.path.basename(LOCAL_DOWNLOADED_FILE)}"

    # --- 2. ДЕМОНСТРАЦИЯ CRUD-ОПЕРАЦИЙ ---

    # UPLOAD (загрузка)
    # upload_file(local_file_path=LOCAL_ORIGINAL_FILE, remote_folder_path=REMOTE_WORK_FOLDER)

    # Проверяем содержимое папки
    # list_folder(REMOTE_WORK_FOLDER)

    # DOWNLOAD (Скачивание)
    download_file(remote_file_path=DOWNLOADED_FILE_PATH, local_destination_path=LOCAL_DOWNLOADED_FILE)

    # UPDATE (Обновление) - просто загружаем другой файл по тому же пути
    # upload_file(local_file_path=LOCAL_UPDATED_FILE, remote_folder_path=REMOTE_WORK_FOLDER)

    # Снова скачиваем, чтобы убедиться, что содержимое изменилось
    # download_file(remote_file_path=REMOTE_FILE_PATH, local_destination_path=LOCAL_DOWNLOADED_FILE)

    # DELETE (Удаление)
    # delete_file(remote_file_path=REMOTE_FILE_PATH)

    # Снова проверяем содержимое папки
    # list_folder(REMOTE_WORK_FOLDER)

    # --- 3. ОЧИСТКА ---
    # Собираем все локальные файлы, которые создали, и передаем их на удаление
    # all_local_files_to_clean = [LOCAL_ORIGINAL_FILE, LOCAL_UPDATED_FILE, LOCAL_DOWNLOADED_FILE]
    # cleanup_local_files(all_local_files_to_clean)

    print("\n✅ Демонстрация успешно завершена!")
