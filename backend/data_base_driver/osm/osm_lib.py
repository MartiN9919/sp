from requests.exceptions import ConnectionError


def osm_search(text):
    """
    Поиск osm-записей
    @param text: поисковая строка
    @return: json [{id,name,icon,},...]
    """
    try:
        print(999, text)
        return [{ 'id': 1, 'name': 'Тест', },]
    except ConnectionError:
        return []
