import os
import asyncio
import json
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist

load_dotenv()

# --- Константа для максимальной длины подписи Telegram ---
MAX_CAPTION_LENGTH = 1024

# --- 1. Загружаем все необходимые переменные ---
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION_NAME')
raw_channel_id = os.getenv('CHANNEL_ID')

if not all([api_id, api_hash, session_name, raw_channel_id]):
    raise ValueError(
        "Пожалуйста, убедитесь, что в файле .env заданы API_ID, API_HASH, SESSION_NAME и CHANNEL_ID"
    )

# --- 2. Преобразуем ID канала в число ---
try:
    CHANNEL_ID = int(raw_channel_id)
    print(f'Используем CHANNEL_ID: {CHANNEL_ID}')
except (ValueError, TypeError):
    raise TypeError("CHANNEL_ID в .env файле должен быть числом (например, -100123456789)")

# Создаем клиент
client = TelegramClient(session_name, int(api_id), api_hash)

def format_message_from_json(info_data):
    """Формирует текстовое сообщение из данных JSON."""
    message_parts = []

    # Название фильма (русское и оригинальное)
    if info_data.get('title_ru'):
        message_parts.append(f"🎬 {info_data['title_ru']}")
    if info_data.get('original_title'):
        message_parts.append(f"©️ {info_data['original_title']}")

    # Жанр
    if info_data.get('genre'):
        message_parts.append(f"🎭 Жанр: {info_data['genre'].capitalize()}")

    # Год
    if info_data.get('year'):
        message_parts.append(f"🗓 Год: {info_data['year']}")

    # Продолжительность
    if info_data.get('duration'):
        message_parts.append(f"⏱️ Продолжительность: {info_data['duration']}")

    # Страна
    if info_data.get('country'):
        message_parts.append(f"🌍 Страна: {info_data['country']}")

    # Режиссер
    if info_data.get('director'):
        message_parts.append(f"🎥 Режиссер: {info_data['director']}")

    # Актеры
    if info_data.get('actors'):
        message_parts.append(f"🤡 Актеры: {info_data['actors']}")

    # Рейтинг Kinopoisk
    if info_data.get('kinopoisk'):
        message_parts.append(f"⭐ Кинопоиск: {info_data['kinopoisk']}")

    # Мировая премьера
    if info_data.get('world_premiere'):
        message_parts.append(f"🌐 Премьера в мире: {info_data['world_premiere']}")

    # Слоган
    if info_data.get('slogan'):
        message_parts.append(f"🗣️ Слоган: {info_data['slogan']}")

    # Описание (добавляем его в конце, если нужно)
    # Описание может быть длинным, поэтому добавляем его последним и обрабатываем отдельно
    description = info_data.get('description')
    if description:
        # Добавляем разделитель перед описанием, если есть другие поля
        if message_parts:
            message_parts.append("") # Пустая строка для отступа

        # Обрезаем описание, если оно слишком длинное, чтобы уложиться в лимит Telegram
        # Оставляем место для уже добавленных полей
        current_length_of_parts = sum(len(p) for p in message_parts) + len(message_parts) # + len(message_parts) за счет '\n'

        remaining_length = MAX_CAPTION_LENGTH - current_length_of_parts - len("📝 Описание:\n") - len("...")

        if remaining_length > 0:
            if len(description) > remaining_length:
                description_trimmed = description[:remaining_length].rsplit(' ', 1)[0] + "..." # Обрезаем по слову
                message_parts.append(f"📝 Описание:\n{description_trimmed}")
                print("Внимание: Описание было обрезано из-за превышения лимита Telegram.")
            else:
                message_parts.append(f"📝 Описание:\n{description}")
        else:
            print("Внимание: Описание не может быть добавлено, так как другие поля уже занимают слишком много места.")


    return "\n".join([part for part in message_parts if part.strip()]) # Убираем пустые строки

async def main(film_path=r'downloads\10-lyudi-v-chernom-2-2002'):
    try:
        # --- Получаем "сущность" (entity) для канала ---
        print(f"\nПопытка найти сущность для канала ID: {CHANNEL_ID}...")
        channel_entity = await client.get_entity(CHANNEL_ID)
        print("Сущность канала успешно найдена!")

        # --- Читаем info.json ---
        info_json_path = os.path.join(film_path, 'info.json')
        if not os.path.exists(info_json_path):
            print(f"Ошибка: Файл info.json не найден по пути: {info_json_path}")
            return

        with open(info_json_path, 'r', encoding='utf-8') as f:
            film_info = json.load(f)

        # --- Формируем сообщение ---
        formatted_message = format_message_from_json(film_info)
        if not formatted_message:
            print("Сформированное сообщение пустое. Проверьте данные в info.json.")
            return

        # --- Отправляем сообщение с картинкой в канал ---
        print("\nОтправка сообщения с картинкой в канал...")

        image_path = os.path.join(film_path, 'poster.jpg')

        if not os.path.exists(image_path):
            print(f"Ошибка: Файл изображения не найден по пути: {image_path}")
            print("Пожалуйста, убедитесь, что указали правильный путь к изображению.")
            return

        channel_post = await client.send_message(
            entity=channel_entity,
            message=formatted_message,
            file=image_path
        )
        print(f"Пост с картинкой и описанием успешно отправлен в канал. ID сообщения: {channel_post.id}")

    except rpcerrorlist.PeerIdInvalidError:
        print(f"Ошибка: неверный ID канала ({CHANNEL_ID}), либо у вас нет к нему доступа.")
    except ValueError as e:
        print(f"Ошибка: не удалось найти чат. Проверьте правильность ID. {e}")
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден. Проверьте путь. {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении файла info.json: проверьте его формат. {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# --- Конструкция if __name__ == '__main__': ---
if __name__ == '__main__':
    try:
        with client:
            client.loop.run_until_complete(main())
    except Exception as e:
        print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

    print("\nРабота клиента завершена.")