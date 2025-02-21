from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

def index(request):
    return render(request, "index.html", {"title": "Welcome to Frontend"})

def auth(request):
    return render(request, "vk_auth.html")

@login_required
def user_data_api(request):
    """Возвращает JSON-ответ с данными авторизованного пользователя"""
    user = request.user
    social = user.social_auth.filter(provider='vk-oauth2').first()

    user_data = {
        'username': user.username,
        'email': user.email,
        'vk_id': social.uid if social else None,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    return JsonResponse(user_data)


def logout_view(request):
    """Выход из системы"""
    logout(request)
    return render(request, 'vk_auth.html')
