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
from django.contrib.auth.decorators import login_required
from .models import Product
from account.models import CustomUser

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

# ==========================================================
# VIEW 1: Untuk mengambil DAFTAR produk (GET list)
# ==========================================================
# (View ini tidak berubah dari sebelumnya)
@require_http_methods(["GET"])
def product_api_view(request):
    # ... (logika filter, sort, pagination tetap sama) ...
    queryset = Product.objects.select_related('user').all()
    # ... (kode filter disembunyikan untuk keringkasan) ...
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
        'is_admin': request.user.is_staff if request.user.is_authenticated else False,
        'results': results
    }
    return JsonResponse(response_data)


# ==========================================================
# VIEW 2: (BARU) Create Product (Hanya POST)
# ==========================================================
@login_required
@require_http_methods(["POST"])
def product_create_view(request):
    """
    API view hanya untuk MEMBUAT (Create) produk baru.
    """
    # Cek izin seller/admin
    if not (request.user.is_admin or request.user.is_seller):
         return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk menambah produk.'}), content_type='application/json')

    try:
        new_product = Product(
            user=request.user,
            name=request.POST.get('name'),
            price=int(request.POST.get('price')),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            thumbnail=request.POST.get('thumbnail', None) or None
        )
        if not new_product.name or not new_product.price or not new_product.category or not new_product.description:
            return HttpResponseBadRequest(json.dumps({'error': 'Semua field wajib (kecuali thumbnail) harus diisi.'}), content_type='application/json')
            
        new_product.save()
        return JsonResponse({'success': True, 'id': new_product.id}, status=201)
    except (ValueError, TypeError):
         return HttpResponseBadRequest(json.dumps({'error': 'Data harga tidak valid.'}), content_type='application/json')
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)


# ==========================================================
# VIEW 3: (BARU) Get Product Detail (Hanya GET)
# ==========================================================
@login_required # Diperlukan agar user bisa mengisi form edit
@require_http_methods(["GET"])
def product_detail_view(request, pk):
    """
    API view hanya untuk MENDAPATKAN (Read) detail satu produk.
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Cek otorisasi (hanya admin/pemilik yang boleh lihat detail untuk edit)
    is_owner = (product.user == request.user)
    is_admin = request.user.is_staff
    if not (is_owner or is_admin):
         return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk melihat detail produk ini.'}), content_type='application/json')

    data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category': product.category,
        'description': product.description,
        'thumbnail': product.thumbnail or '',
    }
    return JsonResponse(data)


# ==========================================================
# VIEW 4: (BARU) Update Product (Hanya POST)
# ==========================================================
@login_required
@require_http_methods(["POST"]) # Menggunakan POST untuk Update
def product_update_view(request, pk):
    """
    API view hanya untuk MEMPERBARUI (Update) produk.
    Menggunakan method POST.
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Cek otorisasi (hanya admin/pemilik)
    is_owner = (product.user == request.user)
    is_admin = request.user.is_staff
    if not (is_owner or is_admin):
        return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk mengubah produk ini.'}), content_type='application/json')
        
    try:
        # Karena ini POST, data ada di request.POST. Ini lebih sederhana!
        data = request.POST
        product.name = data.get('name')
        product.price = int(data.get('price'))
        product.category = data.get('category')
        product.description = data.get('description')
        product.thumbnail = data.get('thumbnail', None) or None
        
        if not product.name or not product.price or not product.category or not product.description:
            return HttpResponseBadRequest(json.dumps({'error': 'Semua field wajib (kecuali thumbnail) harus diisi.'}), content_type='application/json')
        
        product.save()
        return JsonResponse({'success': True})
    except (ValueError, TypeError):
         return HttpResponseBadRequest(json.dumps({'error': 'Data harga tidak valid.'}), content_type='application/json')
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)


# ==========================================================
# VIEW 5: (BARU) Delete Product (Hanya POST)
# ==========================================================
@login_required
@require_http_methods(["POST"]) # Menggunakan POST untuk Delete
def product_delete_view(request, pk):
    """
    API view hanya untuk MENGHAPUS (Delete) produk.
    Menggunakan method POST.
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Cek otorisasi (hanya admin/pemilik)
    is_owner = (product.user == request.user)
    is_admin = request.user.is_staff
    if not (is_owner or is_admin):
        return HttpResponseForbidden(json.dumps({'error': 'Anda tidak punya izin untuk menghapus produk ini.'}), content_type='application/json')

    try:
        product.delete()
        return JsonResponse({'success': True}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
