from django.shortcuts import render

from article.models import News
from product.models import Product

def home(request):
    recent_articles = News.objects.order_by("-created_at").all()[:3]
    featured_products = Product.objects.filter(is_featured=True).all()[:5]
    return render(request, "main-home.html", {
        "articles": recent_articles,
        "products": featured_products
    })


