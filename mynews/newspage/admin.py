from django.contrib import admin

# Register your models here.

from .models import News, Author

class NewsInfo(admin.ModelAdmin):
    list_display=['pk','news_title','author','pub_date']
class AuthorInfo(admin.ModelAdmin):
    list_display=['pk','author_name']

admin.site.register(News,NewsInfo)
admin.site.register(Author,AuthorInfo)