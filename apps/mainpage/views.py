from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests  # Для работы с внешними API

def index(request):
    """Отображает главную страницу"""
    print("Отображаем главную страницу")
    return render(request, "index.html", {"title": "Welcome to Frontend"})

def auth(request):
    """Отображает страницу авторизации"""
    print("Отображаем страницу auth")
    return render(request, "vk_auth.html")

def user_data_api(request):
    """
    Возвращает JSON-ответ с данными пользователя, полученными из VK API.
    Предполагается, что токен передаётся через GET-параметр от фронтенда.
    """
    print("Заходим в метод user_data_api")
    # Получаем токен из запроса (предоставляется клиентским JS)
    access_token = request.GET.get('access_token')
    print("Получен токен:", access_token)
    if not access_token:
        return JsonResponse({'error': 'No access token provided'}, status=400)

    # Запрос к VK API для получения данных пользователя
    vk_api_url = "https://api.vk.com/method/users.get"
    params = {
        'access_token': access_token,
        'v': '5.131',  # Версия API
        'fields': 'first_name,last_name,email',  # Поля, которые нужны
    }

    try:
        print("Отправляем запрос к VK API")
        response = requests.get(vk_api_url, params=params)
        print("Ответ от VK:", response.text)
        response.raise_for_status()  # Проверка на ошибки HTTP
        vk_data = response.json()

        if 'response' not in vk_data or not vk_data['response']:
            return JsonResponse({'error': 'Invalid VK response'}, status=400)

        user_info = vk_data['response'][0]
        user_data = {
            'username': f"vk_{user_info['id']}",  # Формируем псевдо-username
            'vk_id': user_info['id'],
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', ''),
            'email': user_info.get('email', ''),  # Email доступен только если разрешён приложением
        }

        print("Полученные данные пользователя:", user_data)

        return JsonResponse(user_data)

    except requests.RequestException as e:
        print('Что-то пошло не так')

        return JsonResponse({'error': f'Failed to fetch VK data: {str(e)}'}, status=500)

def logout_view(request):
    """Простая заглушка для выхода (без реальной аутентификации)"""
    return render(request, 'vk_logauth.html')