from django.urls import path
from article.views import show_articles

app_name = 'article'

urlpatterns = [
    path('', show_articles, name='show_article'),
]