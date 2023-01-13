from typing import Any

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest


def paginate(request: HttpRequest, posts: Any) -> Any:
    paginator = Paginator(posts, settings.LIMIT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page
