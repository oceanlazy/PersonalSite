from django.shortcuts import render
from .models import Article
from datetime import datetime
from collections import OrderedDict
import math


class Helper:
    RECORDS_ON_PAGE = 5
    DEFAULT_MENU = OrderedDict([('', 'Главная'), ('blog', 'Блог'), ('articles', 'Статьи'), ('contacts', 'Контакты')])

    date = datetime.strftime(datetime.now(), "%A, %d.%m.%Y %H:%M")
    publications = Article.objects.order_by('-published_date')

    @staticmethod
    def page_check(page):
        """Check current page."""
        if page is not None:
            return int(page)
        else:
            return 1

    def articles_prepare(self, cur_page, category=''):
        """Prepare the articles for displaying."""
        if category:
            filtrate = [x for x in self.publications if x.category == category]
            return filtrate[(cur_page - 1) * self.RECORDS_ON_PAGE:cur_page * self.RECORDS_ON_PAGE]
        else:
            return self.publications[(cur_page - 1) * self.RECORDS_ON_PAGE:cur_page * self.RECORDS_ON_PAGE]

    def pages_num_check(self, publications=''):
        """How many pages of articles we have."""
        if publications:
            return list(range(1, math.ceil(len(publications) / self.RECORDS_ON_PAGE) + 1))
        else:
            return list(range(1, math.ceil(len(self.publications) / self.RECORDS_ON_PAGE) + 1))


helper = Helper()


def index(request, cur_page=1):
    """Main page of site, non-default is for url like "^index/" ."""
    cur_page = helper.page_check(cur_page)
    publications = helper.articles_prepare(cur_page)
    pages_num = helper.pages_num_check()
    return render(request, 'index.html', {'date': helper.date, 'publications': publications, 'pages_num': pages_num,
                                          'cur_page': cur_page, 'root': 'index', 'menu_items': helper.DEFAULT_MENU})


def blog(request, cur_page=1):
    cur_page = helper.page_check(cur_page)
    publications = helper.articles_prepare(cur_page, 'блог')
    pages_num = helper.pages_num_check(publications)
    return render(request, 'index.html', {'date': helper.date, 'publications': publications, 'pages_num': pages_num,
                                          'cur_page': cur_page, 'root': 'blog', 'menu_items': helper.DEFAULT_MENU})


def articles(request, cur_page=1):
    menu_items = OrderedDict([('', 'Главная'), ('python', 'Python'), ('articles', 'SQL'), ('contacts', 'RenPy')])
    cur_page = helper.page_check(cur_page)
    publications = helper.articles_prepare(cur_page, 'articles_desc')
    return render(request, 'index.html',
                  {'date': helper.date, 'publications': publications, 'pages_num': list(range(1)),
                   'cur_page': cur_page, 'root': 'articles', 'menu_items': menu_items})


def python(request, cur_page=1):
    menu_items = OrderedDict([('', 'Главная'), ('django', 'Django'), ('pycharm', 'PyCharm'), ('git', 'Git'),
                              ('class', 'Классы'), ('generator', 'Генераторы')])
    cur_page = helper.page_check(cur_page)
    publications = helper.articles_prepare(cur_page, 'python')
    pages_num = helper.pages_num_check(publications)
    return render(request, 'index.html', {'date': helper.date, 'publications': publications, 'pages_num': pages_num,
                                          'cur_page': cur_page, 'root': 'articles', 'menu_items': menu_items})


def contacts(request, cur_page=1):
    cur_page = helper.page_check(cur_page)
    publications = helper.articles_prepare(cur_page, 'contacts')
    return render(request, 'index.html',
                  {'date': helper.date, 'publications': publications, 'pages_num': list(range(1)),
                   'cur_page': cur_page, 'root': 'contacts', 'menu_items': helper.DEFAULT_MENU})
