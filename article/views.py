from django.shortcuts import render, redirect, get_object_or_404
from article.forms import NewsForm
from article.models import News

from django.http import HttpResponse
from django.core import serializers

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
def show_article(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        news_list = News.objects.all()
    elif filter_type == "my":
        news_list = News.objects.filter(user=request.user)
    elif filter_type == "featured":
        news_list = News.objects.filter(is_featured=True)
    elif filter_type == "hot":
        news_list = News.objects.filter(is_news_hot=True)
    elif filter_type == "update":
        news_list = News.objects.filter(category="update")
    elif filter_type == "transfer":
        news_list = News.objects.filter(category="transfer")
    elif filter_type == "exclusive":
        news_list = News.objects.filter(category="exclusive")
    elif filter_type == "match":
        news_list = News.objects.filter(category="match")
    elif filter_type == "rumor":
        news_list = News.objects.filter(category="rumor")
    elif filter_type == "analysis":
        news_list = News.objects.filter(category="analysis")


    context = {
        'title' : 'Sports-zone',
        'news_list' : news_list,
        'username' : request.user.username,
    }
    return render(request, "article.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        form.save()
        return redirect('article:show_article')

    context = {'form': form}
    return render(request, "create_news.html", context)

def show_detail(request, id):
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
   
def edit_article(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('article:show_article')

    context = {
        'form': form
    }

    return render(request, "edit_news.html", context)

def delete_article(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('article:show_article'))

@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    content = strip_tags(request.POST.get("content"))
    category = request.POST.get("category")
    sports_type = strip_tags(request.POST.get("sports_type"))
    thumbnail = strip_tags(request.POST.get("thumbnail"))
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_product = News(
        title=title, 
        content=content,
        category=category,
        sports_type=sports_type,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def edit_news_entry_ajax(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        news.title = strip_tags(request.POST.get("title", news.title))
        news.content = strip_tags(request.POST.get("content", news.content))
        news.category = request.POST.get("category", news.category)
        news.sports_type = strip_tags(request.POST.get("sports_type", news.sports_type))
        news.thumbnail = request.POST.get("thumbnail", news.thumbnail)
        news.is_featured = request.POST.get("is_featured", news.is_featured) == 'on'  # checkbox handling

        news.save()
        return JsonResponse({'success': True})
        
    except News.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
@csrf_exempt
@require_GET
def get_news_entry_ajax(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        return JsonResponse({
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'sports_type': news.sports_type,
            'thumbnail': news.thumbnail,
            'is_featured': news.is_featured,
        })
    except News.DoesNotExist:
        return JsonResponse({'error': 'News not found'}, status=404)