from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # При переходе на главную вызываем соотв. файл
]

handler404 = 'main.views.error_404'
