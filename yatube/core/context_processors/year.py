import datetime

from django.http import HttpRequest


def year(request: HttpRequest) -> dict[str, int]:
    """Добавляет переменную с текущим годом.
    Args:
        request: Любой запрос на сайт,
        что гарантирует выполнение функции во всех случаях.

    Returns:
        Функция возвращает словарь с ключом 'year'.
        Будем использовать ее в footer
    """
    del request
    return {
        'year': datetime.date.today().year,
    }
