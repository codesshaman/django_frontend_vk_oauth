from .views import index, user_data_api, logout_view
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user-data/', user_data_api, name='user_data_api'),  # API-метод для получения данных
    path('logout/', logout_view, name='logout'),
]