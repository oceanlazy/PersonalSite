#!/usr/local/bin/python
# coding=utf-8

from django.shortcuts import render, redirect
from .models import Publication
from collections import OrderedDict
from django.utils import timezone
import math


class Helper:
    RECORDS_ON_PAGE = 5
    PAGE_DATE = timezone.now()
    DEFAULT_MENU = OrderedDict([('Главная', ''), ('Блог', 'blog'), ('Статьи', 'articles'), ('Контакты', 'contacts')])
    library_menus = {
        'articles': OrderedDict([('Python', 'articles/python'), ('SQL', 'articles/sql')]),
        'python': OrderedDict([('Django', 'articles/python/django')]),
    }

    @staticmethod
    def page_check(page):
        """Check current page."""
        if page is not None:
            return int(page)
        else:
            return 1

    def get_content(self, cur_page, publications):
        """Prepare the articles for displaying."""
        return publications[(cur_page - 1) * self.RECORDS_ON_PAGE: cur_page * self.RECORDS_ON_PAGE]

    def pages_num(self, publications=''):
        """How many pages of publications we have."""
        if publications:
            return list(range(1, math.ceil(len(publications) / self.RECORDS_ON_PAGE) + 1))
        else:
            return list(
                range(1, math.ceil(len(Publication.objects.order_by('-published_date')) / self.RECORDS_ON_PAGE) + 1))

    def get_menu(self, slug, slug_prev=''):
        menu = OrderedDict([('Главная', '')])
        try:
            menu.update(self.library_menus[slug])
        except KeyError:
            try:
                menu.update(self.library_menus[slug_prev])
            except KeyError:
                menu = self.DEFAULT_MENU
        return menu



helper = Helper()


def index(request, cur_page=1):
    """Main page of site, non-default is for url like "/" ."""
    cur_page = helper.page_check(cur_page)
    publications = Publication.objects.filter().order_by('-published_date')
    pages_num = helper.pages_num()
    page = helper.get_content(cur_page, publications)
    return render(request, 'headers.html',
                  {'date': helper.PAGE_DATE, 'page': page, 'pages_num': pages_num,
                   'cur_page': cur_page, 'root': 'index', 'menu_items': helper.DEFAULT_MENU})


def blog(request, cur_page):
    cur_page = helper.page_check(cur_page)
    publications = Publication.objects.filter(tags__contains='blog').order_by('-published_date')
    pages_num = helper.pages_num(publications)
    page = helper.get_content(cur_page, publications)
    return render(request, 'posts.html',
                  {'date': helper.PAGE_DATE, 'page': page, 'pages_num': pages_num,
                   'cur_page': cur_page, 'root': 'blog', 'menu_items': helper.DEFAULT_MENU})


def publication(request, slug):
    return render(request, 'publication.html', {'publication': Publication.objects.get(slug=slug),
                                                'date': helper.PAGE_DATE,
                                                'menu_items': helper.DEFAULT_MENU})


def articles(request, slug_1, slug_2, page):
    root = 'articles'
    if not slug_1:
        slug_1 = 'articles'
    else:
        if slug_1.isdigit():
            page = slug_1
            slug_1 = 'articles'
        root = 'articles/{}'.format(slug_1)
    content = Publication.objects.filter(tags__contains=slug_1).order_by('-published_date')
    menu = helper.get_menu(slug_1)
    if slug_2:
        if slug_2.isdigit():
            page = int(slug_2)
        else:
            content = Publication.objects.filter(tags__contains=slug_2).order_by('-published_date')
            menu = helper.get_menu(slug_2, slug_1)
            root = '{}_{}'.format(slug_1, slug_2)
    cur_page = helper.page_check(page)
    pages_num = helper.pages_num(content)
    content = helper.get_content(cur_page, content)
    return render(request, 'headers.html',
                  {'date': helper.PAGE_DATE, 'page': content, 'pages_num': pages_num,
                   'cur_page': cur_page, 'root': root, 'menu_items': menu})


def contacts(request):
    return render(request, 'description.html', {'publication': Publication.objects.get(slug='kontakty'),
                                                'date': helper.PAGE_DATE,
                                                'menu_items': helper.DEFAULT_MENU})
