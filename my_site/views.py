from django.shortcuts import render
from django.utils import timezone
from .models import Article
from datetime import datetime


def index(request):
    date = datetime.strftime(datetime.now(), "%A, %d.%m.%Y %H:%M")
    return render(request, 'main.html', {'date': date})


def blog(request):
    date = datetime.strftime(datetime.now(), "%A, %d.%m.%Y %H:%M")
    articles = Article.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog.html', {'date': date, 'articles': articles})
