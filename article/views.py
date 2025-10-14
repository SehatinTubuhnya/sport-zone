from django.shortcuts import render
from article.models import News

# Create your views here.
def show_articles(request):
    news_list = News.objects.all()
    context = {
        'title' : 'Sports-zone',
        'news_list' : news_list,
    }
    return render(request, "article.html", context)