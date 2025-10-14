from django.urls import path
from article.views import show_article, create_news, show_news 

from article.views import show_xml, show_json
from article.views import show_xml_by_id, show_json_by_id

from article.views import edit_news, delete_news

app_name = 'article'

urlpatterns = [
    path('', show_article, name='show_article'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news, name='show_news'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),
]