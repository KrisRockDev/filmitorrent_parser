import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist  # Импортируем для более точной обработки ошибок

# Загружаем переменные окружения из файла .env
load_dotenv()

# Считываем значения из .env.
# Не забудьте использовать ваши собственные значения с my.telegram.org!
# https://docs.telethon.dev/en/stable/basic/quick-start.html

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
CHAT_ID = os.getenv('CHAT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
GRUP_ID = os.getenv('GRUP_ID')
USER_NAME = os.getenv('USER_NAME')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
session_name = os.getenv('SESSION_NAME')

# Проверяем, что все переменные окружения были загружены
if not all([api_id, api_hash, session_name]):
    raise ValueError("Пожалуйста, убедитесь, что в файле .env заданы API_ID, API_HASH и SESSION_NAME")

# Создаем клиент Telegram
# Файл сессии (session_name.session) будет создан для хранения авторизации
client = TelegramClient(session_name, int(api_id), api_hash)


async def main():
        # --- Блок получения информации о себе ---
    if False:
        try:
            # Получение информации о себе
            me = await client.get_me()

            # "me" - это объект пользователя. Вы можете красиво распечатать
            # любой объект Telegram с помощью метода "stringify":
            print("--- Информация о пользователе ---")
            print(me.stringify())

            # Когда вы что-то печатаете, вы видите его представление.
            # Вы можете получить доступ ко всем атрибутам объектов Telegram
            # с помощью точечной нотации. Например, чтобы получить имя пользователя:
            username = me.username
            print(f"Имя пользователя: {username}")
            print(f"Номер телефона: {me.phone}")
            print("-" * 20)

        except Exception as e:
            print(f"Произошла ошибка при получении информации о себе: {e}")

        # --- Блок перебора диалогов ---
    if True:
        try:
            # Вы можете вывести все диалоги/чаты, в которых вы состоите:
            print("\n--- Список диалогов ---")
            async for dialog in client.iter_dialogs():
                print(f'"{dialog.name}" имеет ID: {dialog.id}')
            print("-" * 20)
        except Exception as e:
            print(f"Произошла ошибка при получении списка диалогов: {e}")

        # --- Блок отправки сообщений ---
    if True:
        try:
            # Вы можете отправлять сообщения себе...
            # await client.send_message('me', 'Привет, это я!')
            # print("\nСообщение отправлено себе.")

            # ...в какой-либо чат по ID (не работает)
            # await client.send_message(CHAT_ID, 'Привет, группа!')
            # print(f"\nСообщение отправлено в CHAT_ID={CHAT_ID}.")

            # ...в какой-либо чат по ID (не работает)
            await client.send_message(CHANNEL_ID, 'Привет, группа!')
            print(f"\nСообщение отправлено в CHANNEL_ID={CHANNEL_ID}.")

            # ...в какой-либо чат по ID (не работает)
            # await client.send_message(GRUP_ID, 'Привет, группа!')
            # print(f"\nСообщение отправлено в GRUP_ID={GRUP_ID}.")

            # ...вашим контактам по номеру телефона (не работает)
            # await client.send_message('+79127052438', 'Привет, друг!')

            # ...или даже любому пользователю по его @username
            # await client.send_message(USER_NAME, 'Тестирую библиотеку Telethon!')
            # print(f"Сообщение отправлено пользователю @{USER_NAME}.")

        # Можно обрабатывать конкретные ошибки, например, если чат не найден
        except rpcerrorlist.PeerIdInvalidError:
            print("Ошибка: неверный ID чата или пользователь не найден.")
        except Exception as e:
            print(f"Произошла ошибка при отправке сообщений: {e}")

        # --- Блок отправки сообщения с разметкой ---
    if False:
        try:
            # Конечно, вы можете использовать Markdown в своих сообщениях:
            message = await client.send_message(
                USER_NAME,
                'Это сообщение содержит **жирный шрифт**, `моноширинный код`, __курсив__ и '
                '[красивую ссылку на сайт](https://example.com)!',
                link_preview=False  # Отключить предпросмотр ссылки
            )

            # Отправка сообщения возвращает объект отправленного сообщения, который можно использовать
            print("\n--- Отправленное сообщение с разметкой ---")
            print(message.raw_text)

            # Вы можете отвечать на сообщения напрямую, если у вас есть объект сообщения
            await message.reply('Круто!')
            print("Ответ на сообщение отправлен.")
            print("-" * 20)

        except Exception as e:
            print(f"Произошла ошибка при отправке сообщения с разметкой или ответа на него: {e}")

        # --- Блок отправки файла ---
    if False:
        try:
            # Или отправлять файлы, песни, документы, альбомы...
            # Замените путь на реальный путь к вашему файлу
            # await client.send_file(USER_NAME, r'e:\Снимок экрана 2025-06-12 200647.png')
            await client.send_file(USER_NAME, r'e:\Downloads\Создание_интерактивных_презентаций_с_ИИ_.mp4')
            print("\n(Блок отправки файла закомментирован. Раскомментируйте его с реальным путем к файлу.)")
        except FileNotFoundError:
            print("Ошибка: Файл для отправки не найден. Проверьте путь.")
        except Exception as e:
            print(f"Произошла ошибка при отправке файла: {e}")

        # --- Блок получения истории сообщений и скачивания медиа ---
    if False:
        try:
            # Вы можете вывести историю сообщений любого чата:
            print("\n--- История последних сообщений из 'Избранного' (me) ---")
            async for message in client.iter_messages('me', limit=5):  # limit=5 для примера
                print(f"ID сообщения: {message.id}, Текст: {message.text}")

                # Вы также можете скачивать медиа из сообщений!
                # Метод вернет путь, по которому был сохранен файл.
                if message.photo:
                    try:
                        print("Найдено фото, начинается скачивание...")
                        path = await message.download_media()
                        print(f'Файл сохранен в: {path}')  # выводится после завершения загрузки
                    except Exception as download_error:
                        print(f"Не удалось скачать медиа из сообщения {message.id}: {download_error}")
            print("-" * 20)
        except Exception as e:
            print(f"Произошла ошибка при получении истории сообщений: {e}")


# Контекстный менеджер 'with client:' автоматически выполняет client.start()
# при входе и client.disconnect() при выходе из блока.
try:
    with client:
        # Запускаем асинхронную функцию main в цикле событий клиента
        client.loop.run_until_complete(main())
except Exception as e:
    print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

print("\nРабота клиента завершена.")