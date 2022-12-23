from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, DeleteView

from .classificator import MainClassify as MC
from .forms import ArticlesForm, TextsFormSecond, FilterTag
from .models import Articles, TagsModel
from django.http import HttpResponse

# Вызываем здесь html-шаблоны.


def home(request):
    return render(request, 'main/home.html')


def index(request):
    news = Articles.objects.all()     # наш список-набор элементов
    count = news.count()
    choices = TagsModel.objects.all()
    answer = 1
    tags = ''
    if request.method == 'POST':
        answer = int(request.POST.get('filter_by'))

        #tags = "в категории " + str(TagsModel.objects.get(tagId=answer).tagName)
        if answer == 1:
            news = Articles.objects.filter(tag='pc')
        else:
            news = Articles.objects.filter(tag='кино')
        count = news.count()
    # forDifferent = FilterTag()
    context = {
        'title': 'Все новости',
        'news': news,
        'choices': choices,
        'tags': tags,
        'count': count
    }
    return render(request, 'main/index.html', context)


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'main/details_view.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'main/create.html'

    form_class = ArticlesForm


class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news'
    template_name = 'main/delete.html'


def classify(request):
    error = ''
    class_text = ''
    if request.method == 'POST':
        form = TextsFormSecond(request.POST)
        second_form = ArticlesForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("full_text")
            class_text = MC.choose_class(text)
        else:
            error = 'Попробуйте ввести другие данные'
    form = ArticlesForm()
    second_form = ArticlesForm()
    context = {
        'form': form,
        'error': error,
        'predict': class_text
    }
    return render(request, 'main/classify.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()   # сохранение в базу данных
        else:
            error = 'Форма была неверной'
    form = ArticlesForm()

    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)


def my_test_500_view(request):
    # Return an "Internal Server Error" 500 response code.
    return HttpResponse(status=500)


def showAll(request):
    news = Articles.objects.all()
    count = news.count()
    return index(request)
