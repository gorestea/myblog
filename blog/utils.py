from django.db.models import Count
from .models import *

menu = [{'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Добавить статью', 'url_name': 'add_page'}]

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('post'))
        user_menu = menu.copy()
        context['menu'] = user_menu
        context['category'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context