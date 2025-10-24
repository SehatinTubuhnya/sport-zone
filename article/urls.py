from django.urls import path
from article.views import show_article, create_news, show_detail

from article.views import show_xml, show_json
from article.views import show_xml_by_id, show_json_by_id

from article.views import edit_article, delete_article

from article.views import add_news_entry_ajax, edit_news_entry_ajax
from article.views import get_news_entry_ajax, delete_news_entry_ajax
from article.views import get_username_by_id

app_name = 'article'

urlpatterns = [
    path('', show_article, name='show_article'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_detail, name='show_detail'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('news/<uuid:id>/edit', edit_article, name='edit_article'),
    path('news/<uuid:id>/delete', delete_article, name='delete_article'),

    path('add-news-ajax', add_news_entry_ajax, name='add_news_entry_ajax'),
    path('delete-news-ajax/<uuid:product_id>', delete_news_entry_ajax, name='delete_news_entry_ajax'),
    path('get-news-ajax/<uuid:news_id>', get_news_entry_ajax, name='get_news_ajax'),
    path('edit-news-ajax/<uuid:news_id>', edit_news_entry_ajax, name='edit_news_entry_ajax'),
    # path('login-ajax/', login_ajax, name='login-ajax'),
    # path('register-ajax/', register_ajax, name='register-ajax'),
    # path('logout-ajax/', logout_ajax, name='logout-ajax'),

    path('get-username-by-id/<int:id>', get_username_by_id, name='get_username-by-id'),
]