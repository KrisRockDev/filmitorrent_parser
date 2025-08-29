import json
import os


def json_write(user_data, json_file_path):
    # Запись данных в JSON-файл
    # print(f"--- ЗАПИСЬ ДАННЫХ В ФАЙЛ '{json_file_path}' ---")

    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            # json.dump() записывает объект Python в файл
            # ensure_ascii=False - говорит не экранировать не-ASCII символы (сохраняет кириллицу)
            # encoding='utf-8' - указывает кодировку файла
            # indent=4 - делает файл читаемым, добавляя отступы
            json.dump(user_data, f, ensure_ascii=False, indent=4)

        # print("✔️ Данные пользователя успешно сохранены в файл.")
        # print("Содержимое файла:")
        # # Выводим содержимое файла для наглядности
        # with open(json_file_path, 'r', encoding='utf-8') as f:
        #     print(f.read())

    except IOError as e:
        print(f"❌ Ошибка при записи файла: {e}")


def json_read():
    # Чтение данных из JSON-файла

    print(f"\n--- ЧТЕНИЕ ДАННЫХ ИЗ ФАЙЛА '{json_file_path}' ---")

    # Проверяем, существует ли файл перед чтением
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                # json.load() читает данные из файла и преобразует их в объект Python
                loaded_user_data = json.load(f)

            print("✔️ Данные успешно загружены из файла.")
            print("\nТип загруженных данных:", type(loaded_user_data))

            # Теперь можно работать с данными как с обычным словарем Python
            print("\n--- Информация о пользователе ---")
            print(f"Имя: {loaded_user_data.get('имя')}")
            print(f"Город: {loaded_user_data.get('город')}")
            print(f"Первый навык: {loaded_user_data.get('навыки', [])[0]}")

        except json.JSONDecodeError as e:
            print(f"❌ Ошибка декодирования JSON: {e}")
        except IOError as e:
            print(f"❌ Ошибка при чтении файла: {e}")
    else:
        print(f"⚠️ Файл '{json_file_path}' не найден.")


if __name__ == '__main__':
    # Используем словарь Python для представления данных
    user_data = {
        "id": 123,
        "имя": "Иван",
        "фамилия": "Петров",
        "город": "Москва",
        "должность": "Инженер-программист",
        "навыки": ["Python", "Базы данных", "Облачные технологии"],
        "активен": True
    }

    # Имя файла для сохранения
    json_file_path = 'user_data_cyrillic.json'

    json_write(user_data, json_file_path)
