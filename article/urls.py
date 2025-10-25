from django.urls import path
from article.views import show_article, show_detail

from article.views import show_json, show_json_by_id

from article.views import add_news_entry_ajax, edit_news_entry_ajax
from article.views import get_news_entry_ajax, delete_news_entry_ajax
from article.views import get_username_by_id, add_comment_entry_ajax
from article.views import show_comment_json_by_news_id

app_name = 'article'

urlpatterns = [
    path('', show_article, name='show_article'),
    path('news/<str:id>/', show_detail, name='show_detail'),
    path('json/', show_json, name='show_json'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),

    path('add-news-ajax', add_news_entry_ajax, name='add_news_entry_ajax'),
    path('delete-news-ajax/<uuid:product_id>', delete_news_entry_ajax, name='delete_news_entry_ajax'),
    path('get-news-ajax/<uuid:news_id>', get_news_entry_ajax, name='get_news_ajax'),
    path('edit-news-ajax/<uuid:news_id>', edit_news_entry_ajax, name='edit_news_entry_ajax'),

    path('get-username-by-id/<int:id>', get_username_by_id, name='get_username-by-id'),
    path('add-comment-ajax/<uuid:news_id>', add_comment_entry_ajax, name='add-comment-ajax'),
    path('get-comment-by-id/<uuid:news_id>', show_comment_json_by_news_id, name='get-comment-by-id')
]