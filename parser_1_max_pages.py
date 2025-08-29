import requests
from bs4 import BeautifulSoup
from settings import FILMITORRENT_URL

def get_max_page_number():
    """
    Парсит веб-страницу, находит блок пагинации и возвращает максимальный номер страницы.

    :param url: URL-адрес страницы для парсинга.
    :return: Максимальный номер страницы в виде строки или None, если не найден.
    """

    try:
        # Отправляем GET-запрос на указанный URL
        response = requests.get(FILMITORRENT_URL)
        response.raise_for_status()  # Проверяем, успешен ли запрос

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим блок навигации по классу и атрибуту align
        navigation_block = soup.find('div', attrs={'class': 'navigation', 'align': 'center'})

        if navigation_block:
            # Находим все ссылки <a> внутри этого блока
            page_links = navigation_block.find_all('a')

            if page_links:
                # Предполагаем, что ссылка на последнюю страницу - это предпоследний тег <a>
                # перед ссылкой "->"
                last_page_link = page_links[-2]
                max_page_number = last_page_link.get_text(strip=True)
                return int(max_page_number)
            else:
                return None
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к URL: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return None

if __name__ == "__main__":
    max_page = get_max_page_number(FILMITORRENT_URL)

    if max_page:
        print(f"Максимальное количество страниц: {max_page}, тип {type(max_page)}")
    else:
        print("Не удалось найти максимальное количество страниц.")