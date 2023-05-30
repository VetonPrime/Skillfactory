from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имен полей
    list_display = ('title', 'category')


admin.site.register(Post)
admin.site.register(Category)
