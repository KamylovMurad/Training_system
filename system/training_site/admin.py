from django.contrib import admin
from .models import Product, Access, Lesson, View


@admin.register(Product)
class ProdductAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'access']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'duration']
    list_filter = ['product']


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'viewed_time', 'viewed']