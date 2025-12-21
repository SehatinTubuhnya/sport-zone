import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from custom_admin.models import ActionLog
from .models import Product


# ================= LIST PRODUCT =================
@require_http_methods(["GET"])
def product_api_view(request):
    queryset = Product.objects.select_related("user").all()

    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    paginator = Paginator(queryset.order_by("-id"), 9)
    page = paginator.get_page(request.GET.get("page", 1))

    results = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "category": p.category,
            "thumbnail": p.thumbnail or "",
            "is_featured": p.is_featured,
            "seller_name": p.user.username if p.user else "Toko Resmi",
            "seller_id": p.user.id if p.user else None,
        }
        for p in page
    ]

    return JsonResponse({"results": results})


# ================= CREATE PRODUCT =================
@csrf_exempt
@require_http_methods(["POST"])
def product_create_view(request):
    # Jangan pakai @login_required untuk API karena dia redirect HTML
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Unauthorized (belum login)"}, status=401)

    if not (getattr(request.user, "is_admin", False) or getattr(request.user, "is_seller", False)):
        return JsonResponse({"success": False, "error": "Tidak punya izin"}, status=403)

    try:
        name = request.POST.get("name")
        price = request.POST.get("price")
        category = request.POST.get("category")

        if not name or not price or not category:
            return JsonResponse({"success": False, "error": "Field wajib tidak boleh kosong"}, status=400)

        product = Product.objects.create(
            user=request.user,
            name=name,
            price=int(price),
            category=category,
            description=request.POST.get("description", ""),
            thumbnail=request.POST.get("thumbnail") or None,
            is_featured=(request.POST.get("is_featured") == "true"),
        )

        ActionLog.objects.create(
            actor=request.user.username,
            action=f"Membuat produk '{product.name}'",
        )

        return JsonResponse({"success": True, "id": product.id}, status=201)

    except ValueError:
        return JsonResponse({"success": False, "error": "Harga harus angka"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)



# ================= DELETE PRODUCT =================
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not (request.user.is_admin or product.user == request.user):
        return HttpResponseForbidden(
            json.dumps({"error": "Tidak punya izin menghapus"}),
            content_type="application/json",
        )

    name = product.name
    product.delete()

    ActionLog.objects.create(
        actor=request.user.username,
        action=f"Menghapus produk '{name}'",
    )

    return JsonResponse({"success": True})


# ================= JSON UNTUK FLUTTER =================
def show_json(request):
    products = Product.objects.all()
    return JsonResponse({
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description,
                "category": p.category,
                "thumbnail": p.thumbnail or "",
                "is_featured": p.is_featured,
                "seller_name": p.user.username if p.user else "Toko Resmi",
                "seller_id": p.user.id if p.user else None,
            }
            for p in products
        ]
    })
# edit
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Permission: admin boleh edit semua, owner boleh edit miliknya
    # Catatan: kalau product.user None (produk lama), hanya admin yg bisa edit
    is_owner = (product.user == request.user)
    is_admin = getattr(request.user, "is_admin", False)

    if not (is_admin or is_owner):
        return HttpResponseForbidden(
            json.dumps({"error": "Tidak punya izin mengedit produk ini."}),
            content_type="application/json",
        )

    try:
        name = request.POST.get("name", product.name)
        price = request.POST.get("price", product.price)
        category = request.POST.get("category", product.category)

        if not name or not str(price) or not category:
            return HttpResponseBadRequest(
                json.dumps({"error": "Field wajib tidak boleh kosong."}),
                content_type="application/json",
            )

        product.name = name
        product.price = int(price)
        product.category = category
        product.description = request.POST.get("description", product.description or "")
        product.thumbnail = request.POST.get("thumbnail") or None
        product.is_featured = request.POST.get("is_featured") == "true"
        product.save()

        ActionLog.objects.create(
            actor=request.user.username,
            action=f"Mengedit produk '{product.name}'",
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# update product
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # aturan izin: admin/seller/owner (silakan sesuaikan)
    is_owner = (product.user == request.user)
    is_admin = getattr(request.user, "is_admin", False)
    is_seller = getattr(request.user, "is_seller", False)

    if not (is_admin or is_seller or is_owner):
        return HttpResponseForbidden(
            json.dumps({"error": "Tidak punya izin untuk mengedit produk ini."}),
            content_type="application/json",
        )

    try:
        name = request.POST.get("name")
        price = request.POST.get("price")
        category = request.POST.get("category")

        if not name or not price or not category:
            return HttpResponseBadRequest(
                json.dumps({"error": "Field wajib tidak boleh kosong (name, price, category)."}),
                content_type="application/json",
            )

        product.name = name
        product.price = int(price)
        product.category = category
        product.description = request.POST.get("description", "")
        product.thumbnail = request.POST.get("thumbnail") or None

        # Flutter akan kirim "true"/"false"
        product.is_featured = (request.POST.get("is_featured") == "true")

        product.save()

        ActionLog.objects.create(
            actor=request.user.username,
            action=f"Mengedit produk '{product.name}' (id={product.id})",
        )

        return JsonResponse({"success": True}, status=200)

    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"error": "Harga harus angka."}),
            content_type="application/json",
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
