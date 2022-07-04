from django.contrib import admin
from .models import Category, News, PostCategory, Subscribe

# Register your models here.
admin.site.register(Category)
admin.site.register(News)
admin.site.register(PostCategory)
admin.site.register(Subscribe)
