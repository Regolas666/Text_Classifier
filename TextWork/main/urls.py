from django.urls import path
from . import views

# здесь вызывем Views (что у нас должно открываться, опред. html-шаблон)
urlpatterns = [
    path('', views.home, name='home'),
    path('news', views.index, name='news'),
    path('classify', views.classify, name='classify'),
    path('create', views.create, name='create'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='details_view'),
    path('news/<int:pk>/update', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', views.NewsDeleteView.as_view(), name='news_delete')
]
