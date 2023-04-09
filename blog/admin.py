from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'get_html_photo')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
