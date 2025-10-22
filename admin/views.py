from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger
from account.models import CustomUser
from .models import ActionLog
from .utils import admin_only

@admin_only(redirect="/")
def homepage(request: HttpRequest):
    return render(request, "admin/home.html", {})

@admin_only(redirect="/")
def accounts_page(request: HttpRequest):
    return render(request, "admin/accounts.html", {})

@admin_only()
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

    return JsonResponse(datas, safe=False)

@admin_only()
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

@admin_only
def edit_account_api(request: HttpRequest):
    account_id = request.POST.get("id")
    username = request.POST.get("username")
    password = request.POST.get("password")
    is_admin = request.POST.get("is_admin") == "true"
    is_author = request.POST.get("is_author") == "true"
    is_seller = request.POST.get("is_seller") == "true"

    try:
        account = CustomUser.objects.get(id=account_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account not found."}, safe=False)

    account.username = username
    if password:
        account.set_password(password)
    account.is_admin = is_admin
    account.is_author = is_author
    account.is_seller = is_seller
    account.save()

    return JsonResponse({"status": "success"}, safe=False)

@admin_only()
def delete_account_api(request: HttpRequest):
    account_id = request.POST.get("id")

    try:
        account = CustomUser.objects.get(id=account_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account not found."}, safe=False)

    account.delete()
    return JsonResponse({"status": "success"}, safe=False)

@admin_only()
def get_products_api(request: HttpRequest):
    ...

@admin_only()
def edit_product_api(request: HttpRequest):
    ...

@admin_only()
def delete_product_api(request: HttpRequest):
    ...

@admin_only()
def get_action_logs_api(request: HttpRequest):
    per_page = request.GET.get("per_page") or "20"

    try:
        per_page = int(per_page)

        if per_page < 1:
            per_page = 20
    except:
        per_page = 20

    logs = ActionLog.objects.all()
    paginator = Paginator(logs, per_page=per_page)

    page = request.GET.get("page")
    datas = paginator.get_page(page)

    return JsonResponse(datas, safe=False)

@admin_only()
def delete_action_log_api(request: HttpRequest):
    ids = request.POST.getlist("ids")

    ActionLog.objects.filter(id__in=ids).delete()
    return JsonResponse({"status": "success"}, safe=False)

@admin_only()
def purge_action_logs_api(request: HttpRequest):
    ActionLog.objects.all().delete()
    return JsonResponse({"status": "success"}, safe=False)

@admin_only(redirect="/")
def action_logs_page(request: HttpRequest):
    return render(request, "admin/action_logs.html", {})
