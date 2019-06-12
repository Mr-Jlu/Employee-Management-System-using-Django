from django.shortcuts import render


def login_user(request):
    return render(request, 'login.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})
