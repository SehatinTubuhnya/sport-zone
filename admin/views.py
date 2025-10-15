from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger
from account.models import CustomUser
from .models import ActionLog

def homepage(request: HttpRequest):
    return render(request, "admin/home.html", {})

def get_accounts(request: HttpRequest):
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

def get_action_logs(request: HttpRequest):
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
