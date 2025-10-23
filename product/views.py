from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.core import serializers
from django.http import HttpResponse

def create_products(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_products.html", context)

def show_products(request, id):
    products = get_object_or_404(Product, pk=id)

    return render(request, "products_detail.html")

def show_json_by_id(request, products_id):
   try:
       products_item = Product.objects.get(pk=products_id)
       json_data = serializers.serialize("json", [products_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)