from django.http import JsonResponse
from django.shortcuts import render

from article.models import News
from product.models import Product


def home(request):
    recent_articles = News.objects.order_by("-created_at").all()[:3]
    featured_products = Product.objects.filter(is_featured=True).all()[:5]
    return render(
        request,
        "main-home.html",
        {"articles": recent_articles, "products": featured_products},
    )


def api_recent(request):
    recent_articles = News.objects.order_by("-created_at").all()[:3]
    featured_products = Product.objects.filter(is_featured=True).all()[:5]

    article_dict = [
        {
            "title": news.title,
            "category": news.category,
            "sports_type": news.sports_type,
            "thumbnail": news.thumbnail or "",
            "is_featured": news.is_featured,
            "created_at": news.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for news in recent_articles
    ]

    product_dict = [
        {
            "name": product.name,
            "price": product.price,
            "thumbnail": product.thumbnail or "",
            "is_featured": product.is_featured,
        }
        for product in featured_products
    ]

    return JsonResponse({"articles": article_dict, "products": product_dict})
