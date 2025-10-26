from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models.query import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse

import json
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Product
from account.models import CustomUser
from custom_admin.models import ActionLog

def delete_products(request, id):
    products = get_object_or_404(Product, pk=id)
    products.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def edit_products(request, id):
    products = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=products)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_product')

    context = {
        'form': form
    }

    return render(request, "edit_products.html", context)

def show_products_list(request):
    return render(request, "main-product.html", {})

def create_products(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_products.html", context)

def show_product_detail(request, id):
    get_object_or_404(Product, pk=id)

    return render(request, "product-detail.html", { "id": id })

def show_json_by_id(request, products_id):
   try:
       products_item = Product.objects.get(pk=products_id)
       json_data = serializers.serialize("json", [products_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

@require_http_methods(["GET"])
def product_api_view(request):
    queryset = Product.objects.select_related('user').all()

    search_query = request.GET.get('search', None)
    categories = request.GET.getlist('category') 
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    sort_by = request.GET.get('sort', 'latest')

    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    if categories:
        queryset = queryset.filter(category__in=categories)
    if min_price:
        try: queryset = queryset.filter(price__gte=int(min_price))
        except ValueError: pass
    if max_price:
        try: queryset = queryset.filter(price__lte=int(max_price))
        except ValueError: pass
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    else: 
        queryset = queryset.order_by('-id')

    page_number = request.GET.get('page', 1)
    products_per_page = 9 
    paginator = Paginator(queryset, products_per_page)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    results = []
    for product in page_obj.object_list:
        results.append({
            'id': str(product.id), 
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail or '', 
            'is_featured': product.is_featured,
            'seller_name': product.user.username if product.user else 'Toko Resmi',
            'seller_id': product.user.id if product.user else None
        })
    response_data = {
        'total_count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'logged_in_user_id': request.user.id if request.user.is_authenticated else None,
        'is_admin': request.user.is_admin if request.user.is_authenticated else False,
        'results': results
    }
    return JsonResponse(response_data)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_create_view(request):
    if not (request.user.is_admin or request.user.is_seller):
         return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk menambah produk.'}), content_type='application/json')

    try:
        new_product = Product(
            user=request.user,
            name=request.POST.get('name'),
            price=int(request.POST.get('price')),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            thumbnail=request.POST.get('thumbnail', None) or None,
            is_featured=request.POST.get('is_featured', 'no') == "on"
        )

        new_product.save()

        log = ActionLog(actor=request.user.username, action=f"Membuat produk dengan nama '{new_product.name}'")
        log.save()

        return JsonResponse({'success': True, 'id': new_product.id}, status=201)
    except (ValueError, TypeError):
         return HttpResponseBadRequest(json.dumps({'error': 'Data harga tidak valid.'}), content_type='application/json')
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def product_detail_view(request, pk):
    product = get_object_or_404(Product.objects.select_related("user"), pk=pk)

    data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category_display': product.get_category_display(),
        'category': product.category,
        'description': product.description,
        'thumbnail': product.thumbnail or '',
        'is_featured': product.is_featured,
        'can_manage': (request.user.is_admin or request.user == product.user) if request.user.is_authenticated else False,
        'seller': {
            'username': product.user.username if product.user else "Toko Resmi",
            'profile_pic': product.user.profile_pic if product.user else ""
        }
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_owner = (product.user == request.user)
    is_admin = request.user.is_admin
    if not (is_owner or is_admin):
        return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk mengubah produk ini.'}), content_type='application/json')
        
    try:
        data = request.POST
 
        product.name = data.get('name')
        product.price = int(data.get('price'))
        product.category = data.get('category')
        product.description = data.get('description')
        product.thumbnail = data.get('thumbnail', None) or None
        product.is_featured = data.get('is_featured', 'no') == 'on'
        product.save()

        log = ActionLog(actor=request.user.username, action=f"Mengedit produk dengan nama '{product.name}'")
        log.save()

        return JsonResponse({'success': True})
    except (ValueError, TypeError):
         return HttpResponseBadRequest(json.dumps({'error': 'Data harga tidak valid.'}), content_type='application/json')
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_owner = (product.user == request.user)
    is_admin = request.user.is_admin
    if not (is_owner or is_admin):
        return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk menghapus produk ini.'}), content_type='application/json')

    try:
        product.delete()

        log = ActionLog(actor=request.user.username, action=f"Menghapus produk dengan nama '{product.name}'")
        log.save()

        return JsonResponse({'success': True}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
