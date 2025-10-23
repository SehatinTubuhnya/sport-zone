from django.http import HttpRequest, HttpResponseRedirect, JsonResponse

def admin_only(redirect: str | False = False):
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.is_admin:
                if redirect:
                    return HttpResponseRedirect(redirect)
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
