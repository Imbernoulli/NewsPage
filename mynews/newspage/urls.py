from django.contrib import admin
from django.urls import path,include
from django.conf import settings

from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path('singlepage/home.html/',views.dirhome),
    path('search/',views.searchpage, name='search'),
    path('allnews/',views.allnews),
    path('cat/',views.cat, name='cat'),
    path('cat/golist/<str:keyword>/',views.kw, name='cat'),
    path('search/list', views.search, name='list'),
    path('search/<int:newsid>', views.page),
    path('create_comment/<int:news_id>/', views.create_comment, name='create_comment'),
    path('delete_comment/<int:comment_id>/<int:news_id>/', views.delete_comment, name='delete_comment'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)