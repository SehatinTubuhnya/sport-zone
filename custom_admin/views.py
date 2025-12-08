from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

from account.models import CustomUser
from product.models import Product
from article.models import News

from .models import ActionLog
from .utils import staff_only

@staff_only(redirect="/")
def homepage(request: HttpRequest):
    return render(request, "admin/home.html", {})

@staff_only(redirect="/")
def accounts_page(request: HttpRequest):
    return render(request, "admin/accounts.html", {})

@staff_only()
def get_summary(request: HttpRequest):
    user_count = CustomUser.objects.all().count()
    article_count = News.objects.all().count()
    product_count = Product.objects.all().count()
    recent_logs = ActionLog.objects.order_by("-timestamp").all()[:5]

    data = {
        "user_count": user_count,
        "article_count": article_count,
        "product_count": product_count,
        "recent_logs": [
            {
                "timestamp": log.timestamp,
                "actor": log.actor,
                "action": log.action
            }
            for log in recent_logs
        ]
    }

    return JsonResponse(data)

@staff_only()
def get_accounts_api(request: HttpRequest):
    accounts = CustomUser.objects

    query = request.GET.get("query")
    if query:
        accounts = accounts.filter(username__icontains=query)

    per_page = request.GET.get("per_page") or "20"

    try:
        per_page = int(per_page)

        if per_page < 1:
            per_page = 20
    except:
        per_page = 20

    accounts = accounts.order_by("username").all()
    paginator = Paginator(accounts, per_page=per_page)

    page = request.GET.get("page")
    datas = paginator.get_page(page)

    result = {
        "total_count": accounts.count(),
        "datas": [
            {
                "id": data.id,
                "profile_pic": data.profile_pic,
                "username": data.username,
                "is_admin": data.is_admin,
                "is_author": data.is_author,
                "is_seller": data.is_seller
            } for data in datas
        ]
    }

    return JsonResponse(result, safe=False)

@staff_only()
def add_account_api(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")
    is_admin = request.POST.get("is_admin") == "true"
    is_author = request.POST.get("is_author") == "true"
    is_seller = request.POST.get("is_seller") == "true"

    if not username or not password:
        return JsonResponse({"status": "error", "message": "Username and password are required."}, safe=False)

    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({"status": "error", "message": "Username already exists."}, safe=False)

    account = CustomUser.objects.create_user(
        username=username,
        password=password
    )

    account.is_admin = is_admin
    account.is_author = is_author
    account.is_seller = is_seller

    account.save()
    return JsonResponse({"status": "success"}, safe=False)

@csrf_exempt
@staff_only()
def edit_account_api(request: HttpRequest):
    account_id = request.POST.get("id")
    username = request.POST.get("username")
    profile_pic = request.POST.get("profile_pic")
    password = request.POST.get("password")
    is_admin = request.POST.get("is_admin") == "on"
    is_author = request.POST.get("is_author") == "on"
    is_seller = request.POST.get("is_seller") == "on"

    try:
        account = CustomUser.objects.get(id=account_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account not found."}, safe=False, status=400)

    account.username = username
    if password:
        account.set_password(password)
    account.profile_pic = profile_pic
    account.is_admin = is_admin
    account.is_author = is_author
    account.is_seller = is_seller
    account.save()

    log = ActionLog.objects.create(actor = request.user.username, action = f"Mengedit user dengan username '{account.username}'")
    log.save()

    return JsonResponse({"status": "success"}, safe=False)

@csrf_exempt
@staff_only()
def delete_account_api(request: HttpRequest):
    account_id = request.POST.get("id")

    try:
        account = CustomUser.objects.get(id=account_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account not found."}, safe=False)

    account.delete()

    log = ActionLog.objects.create(actor = request.user.username, action = f"Menghapus user dengan username '{account.username}'")
    log.save()

    return JsonResponse({"status": "success"}, safe=False)

@staff_only(redirect="/")
def action_logs_page(request: HttpRequest):
    return render(request, "admin/action-logs.html", {})

@staff_only()
def get_action_logs_api(request: HttpRequest):
    per_page = request.GET.get("per_page") or "20"

    try:
        per_page = int(per_page)

        if per_page < 1:
            per_page = 20
    except:
        per_page = 20

    logs = ActionLog.objects.order_by("-timestamp").all()
    paginator = Paginator(logs, per_page=per_page)

    page = request.GET.get("page")
    datas = paginator.get_page(page)

    result = {
        "total_count": logs.count(),
        "datas": [
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "actor": log.actor,
                "action": log.action
            } for log in datas
        ]
    }

    return JsonResponse(result, safe=False)

@csrf_exempt
@staff_only()
def delete_action_log_api(request: HttpRequest):
    ids = request.POST.getlist("ids")

    ActionLog.objects.filter(id__in=ids).delete()
    return JsonResponse({"status": "success"}, safe=False)

@staff_only()
def purge_action_logs_api(request: HttpRequest):
    ActionLog.objects.all().delete()
    return JsonResponse({"status": "success"}, safe=False)
