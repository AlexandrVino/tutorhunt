from typing import Any, Dict
from django.http import HttpRequest

from homepage.forms import SearchForm


def add_searchform(request: HttpRequest) -> Dict[str, Any]:
    """Контекст-процессор для добавления формы поиска"""
    return {"search_form": SearchForm()}
