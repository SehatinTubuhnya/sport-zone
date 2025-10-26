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
from article.models import News

def profile_page_view(request, username):
    get_object_or_404(CustomUser, username=username)
    context = {
        'profile_user_username': username
    }
    return render(request, 'profile.html', context)

@require_http_methods(["GET"])
def profile_detail_api_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    is_self = (request.user == profile_user)

    birth_date_iso = None
    if profile_user.birth_date:
        birth_date_iso = profile_user.birth_date.isoformat() # format YYYY-MM-DD

    data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'profile_pic': profile_user.profile_pic or '',
        'date_joined_display': _date(profile_user.date_joined, "d F Y"),
        'birth_date_display': _date(profile_user.birth_date, "d F Y") if profile_user.birth_date else "-",
        'birth_date_iso': birth_date_iso,
        'is_admin': profile_user.is_admin,
        'is_seller': profile_user.is_seller,
        'is_author': profile_user.is_author,
        'is_self': is_self
    }
    return JsonResponse(data)

@require_http_methods(["GET"])
def profile_content_api_view(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    tab = request.GET.get('tab', 'tentang')
    data = {}
    if tab == 'produk' and profile_user.is_seller:
        products = Product.objects.filter(user=profile_user).order_by('-id')
        serialized_data = [{'id': p.id, 'name': p.name, 'price': p.price, 'category': p.get_category_display(), 'thumbnail': p.thumbnail or ''} for p in products]
        data = {'tab': 'produk', 'data': serialized_data}
    elif tab == 'artikel' and profile_user.is_author:
        try:
            articles = News.objects.filter(user=profile_user).all().order_by('-created_at') 
            serialized_data = [{'id': a.id, 'title': a.title, 'snippet': a.snippet() if hasattr(a, 'snippet') else a.content[:150], 'created_at': a.created_at} for a in articles]
            data = {'tab': 'artikel', 'data': serialized_data}
        except Exception as e:
            data = {'tab': 'artikel', 'data': []}
    else:
        about_text = f"Ini adalah halaman profil untuk {profile_user.username}. Bergabung sejak { _date(profile_user.date_joined, 'd F Y') }."
        data = {'tab': 'tentang', 'data': about_text}
    return JsonResponse(data)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def profile_update_api_view(request):
    user = request.user
    data = request.POST
    new_password = data.get('new_password')

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

    response_data = {
        'success': True,
        'new_data': {
            'profile_pic': user.profile_pic or '',
            'birth_date_display': _date(user.birth_date, "d F Y") if user.birth_date else "-"
        }
    }
    return JsonResponse(response_data)

