from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template.defaultfilters import date as _date
from django.views.decorators.csrf import csrf_exempt
import json

from account.models import CustomUser
from product.models import Product
# from .models import Article # Hapus komentar jika Anda punya model Article

# ==========================================================
# VIEW 1: Me-render Halaman HTML Profile (HANYA skeleton)
# ==========================================================
def profile_page_view(request, username):
    """
    Menampilkan halaman profil.
    View ini HANYA me-render skeleton HTML.
    Data user akan diambil via AJAX.
    """
    # Kita hanya perlu memastikan user ada.
    # Dan kita kirim username ke JS.
    get_object_or_404(CustomUser, username=username)
    context = {
        'profile_user_username': username
    }
    return render(request, 'profile.html', context)

# ==========================================================
# VIEW 2: (BARU) API untuk Data Detail Profile (AJAX GET)
# ==========================================================
@require_http_methods(["GET"])
def profile_detail_api_view(request, username):
    """
    Mengambil data JSON untuk sidebar profil.
    """
    profile_user = get_object_or_404(CustomUser, username=username)
    
    # Cek apakah user yang login sedang melihat profilnya sendiri
    is_self = (request.user == profile_user)
    
    # Format tanggal untuk <input type="date"> (YYYY-MM-DD)
    birth_date_iso = None
    if profile_user.birth_date:
        birth_date_iso = profile_user.birth_date.isoformat() # format YYYY-MM-DD

    data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'profile_pic': profile_user.profile_pic or '',
        'date_joined_display': _date(profile_user.date_joined, "d F Y"),
        'birth_date_display': _date(profile_user.birth_date, "d F Y") if profile_user.birth_date else "-",
        'birth_date_iso': birth_date_iso, # Untuk form modal
        'is_admin': profile_user.is_admin,
        'is_seller': profile_user.is_seller,
        'is_author': profile_user.is_author,
        'is_self': is_self # Penting untuk JS tahu
    }
    return JsonResponse(data)


# ==========================================================
# VIEW 3: API untuk Konten Tab (AJAX GET)
# ==========================================================
# (Tidak ada perubahan pada view ini dari jawaban sebelumnya)
@require_http_methods(["GET"])
def profile_content_api_view(request, user_id):
    # ... (Logika tetap sama)
    profile_user = get_object_or_404(CustomUser, id=user_id)
    tab = request.GET.get('tab', 'tentang')
    data = {}
    if tab == 'produk' and profile_user.is_seller:
        # (Logika ambil produk)
        products = Product.objects.filter(user=profile_user).order_by('-id')
        serialized_data = [{'id': p.id, 'name': p.name, 'price': p.price, 'category': p.get_category_display(), 'thumbnail': p.thumbnail or ''} for p in products]
        data = {'tab': 'produk', 'data': serialized_data}
    elif tab == 'artikel' and profile_user.is_author:
        # (Logika ambil artikel)
        # Hapus/sesuaikan blok try-except ini jika tidak ada model Article
        try:
            articles = profile_user.articles.all().order_by('-created_at') 
            serialized_data = [{'id': a.id, 'title': a.title, 'snippet': a.snippet() if hasattr(a, 'snippet') else a.content[:150], 'created_at': a.created_at} for a in articles]
            data = {'tab': 'artikel', 'data': serialized_data}
        except Exception as e:
            data = {'tab': 'artikel', 'data': []}
    else:
        about_text = f"Ini adalah halaman profil untuk {profile_user.username}. Bergabung sejak { _date(profile_user.date_joined, 'd F Y') }."
        data = {'tab': 'tentang', 'data': about_text}
    return JsonResponse(data)


# ==========================================================
# VIEW 4: API untuk Update Profile (AJAX POST)
# ==========================================================
# (Tidak ada perubahan pada view ini dari jawaban sebelumnya)
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def profile_update_api_view(request):
    # ... (Logika update tetap sama)
    user = request.user
    data = request.POST
    new_password = data.get('new_password')
    # ... (logika validasi password)
    if new_password:
        if new_password != data.get('confirm_password'):
            return HttpResponseBadRequest(json.dumps({'error': 'Password baru dan konfirmasi tidak cocok!'}), content_type='application/json')
        user.set_password(new_password)
    
    try:
        user.profile_pic = data.get('profile_pic') or None
        birth_date = data.get('birth_date')
        user.birth_date = birth_date if birth_date else None
        user.save()
    except Exception as e:
        return JsonResponse({'error': f'Gagal menyimpan data: {e}'}, status=500)

    if new_password:
        update_session_auth_hash(request, user)

    # Kirim kembali data baru (view lama sudah melakukan ini, bagus!)
    response_data = {
        'success': True,
        'new_data': {
            'profile_pic': user.profile_pic or '',
            'birth_date_display': _date(user.birth_date, "d F Y") if user.birth_date else "-"
        }
    }
    return JsonResponse(response_data)

