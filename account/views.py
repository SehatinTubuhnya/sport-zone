from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpRequest
from account.forms import UserForm

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        form = UserForm({
            "username": username,
            "password1": password1,
            "password2": password2
        })

        if form.is_valid():
            form.save()
            return HttpResponse(b"CREATED", status=201)
        else:
            non_field_errors = []
            field_errors = []

            for error in form.non_field_errors():
                non_field_errors.append(str(error))

            for field, errors in form.errors.items():
                if field == "__all__": continue

                for error in errors:
                    field_errors.append({ "field": field, "error": str(error) })

            return JsonResponse({
                "non_field_errors": non_field_errors,
                "field_errors": field_errors
            }, status=400)

    return render(request, 'register.html', {})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        form = AuthenticationForm(data={
            "username": username,
            "password": password
        })

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            response = HttpResponse(b"OK", status=200)

            return response
        else:
            non_field_errors = []
            field_errors = []

            for error in form.non_field_errors():
                non_field_errors.append(str(error))

            for field, errors in form.errors.items():
                if field == "__all__": continue

                for error in errors:
                    field_errors.append({ "field": field, "error": str(error) })

            return JsonResponse({
                "non_field_errors": non_field_errors,
                "field_errors": field_errors
            }, status=400)
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:home')