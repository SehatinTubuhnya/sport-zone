from django.shortcuts import render, redirect, get_object_or_404
from article.forms import NewsForm
from article.models import News

from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_article(request):
    news_list = News.objects.all()
    context = {
        'title' : 'Sports-zone',
        'news_list' : news_list,
    }
    return render(request, "article.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('article:show_news')

    context = {'form': form}
    return render(request, "create_news.html", context)

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)

def show_xml(request):
     news_list = News.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, news_id):
   try:
       news_item = News.objects.filter(pk=news_id)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except News.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json_by_id(request, news_id):
   try:
       news_item = News.objects.get(pk=news_id)
       json_data = serializers.serialize("json", [news_item])
       return HttpResponse(json_data, content_type="application/json")
   except News.DoesNotExist:
       return HttpResponse(status=404)