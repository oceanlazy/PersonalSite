#!/usr/local/bin/python
# coding=utf-8

from django.views.generic import TemplateView
from collections import OrderedDict
from .models import Publication
import math


class Helper:
    RECORDS_ON_PAGE = 5
    LIBRARY_MENUS = {
        'default': OrderedDict([('Главная', ''), ('Блог', 'blog'), ('Статьи', 'articles'), ('Контакты', 'contacts')]),
        'articles': OrderedDict([('Python', 'articles/python'), ('SQL', 'articles/sql')]),
        'python': OrderedDict([('Django', 'articles/python/django')]),
    }

    def get_content(self, cur_page, publications):
        """Prepare the articles for displaying."""
        return publications[(cur_page - 1) * self.RECORDS_ON_PAGE: cur_page * self.RECORDS_ON_PAGE]

    def pages_num(self, publications=''):
        """How many pages of publications we have."""
        return list(range(1, math.ceil(len(publications) / self.RECORDS_ON_PAGE) + 1))

    def get_menu(self, slug, slug_prev='articles'):
        """Get menu or leave menu if not exist."""
        menu = OrderedDict([('Главная', '')])
        try:
            menu.update(self.LIBRARY_MENUS[slug])
        except KeyError:
            menu.update(self.LIBRARY_MENUS[slug_prev])
        return menu


class IndexView(TemplateView, Helper):
    template_name = "headers.html"

    def cur_page_check(self):
        try:
            return int(self.kwargs['cur_page'])
        except (KeyError, TypeError):
            return 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['root'] = 'index'
        context['cur_page'] = self.cur_page_check()
        context['publication'] = Publication.objects.filter().order_by('-published_date')
        context['pages_num'] = self.pages_num(context['publication'])
        context['content_page'] = self.get_content(context['cur_page'], context['publication'])
        context['menu_items'] = self.LIBRARY_MENUS['default']
        return context


class BlogView(TemplateView, Helper):
    template_name = "posts.html"

    def cur_page_check(self):
        try:
            return int(self.kwargs['cur_page'])
        except (KeyError, TypeError):
            return 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = Publication.objects.filter(tags__contains='blog').order_by('-published_date')
        context['cur_page'] = self.cur_page_check()
        context['pages_num'] = self.pages_num(publication)
        context['content_page'] = self.get_content(context['cur_page'], publication)
        context['menu_items'] = self.LIBRARY_MENUS['default']
        return context


class ArticlesView(TemplateView, Helper):
    template_name = "headers.html"

    def cur_page_check(self):
        try:
            return int(self.kwargs['slug_1'])
        except (KeyError, TypeError):
            return 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['root'] = 'articles'
        context['menu_items'] = self.get_menu('articles')
        context['content_page'] = Publication.objects.filter(tags__contains='articles').order_by('-published_date')
        context['cur_page'] = self.cur_page_check()
        context['pages_num'] = self.pages_num(context['content_page'])
        context['content_page'] = self.get_content(context['cur_page'], context['content_page'])
        return context


class ArticlesCategoryView(TemplateView, Helper):
    template_name = "headers.html"

    def cur_page_check(self):
        try:
            return int(self.kwargs['slug_2'])
        except (KeyError, TypeError):
            return 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['root'] = 'articles/{}'.format(kwargs['slug_1'])
        context['menu_items'] = self.get_menu(kwargs['slug_1'])
        context['content_page'] = Publication.objects.filter(tags__contains=kwargs['slug_1']).order_by('-published_date')
        context['cur_page'] = self.cur_page_check()
        context['pages_num'] = self.pages_num(context['content_page'])
        context['content_page'] = self.get_content(context['cur_page'], context['content_page'])
        return context


class ArticlesSubCategoryView(TemplateView, Helper):
    template_name = "headers.html"

    def cur_page_check(self):
        try:
            return int(self.kwargs['slug_3'])
        except (KeyError, TypeError):
            return 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['root'] = 'articles/{}/{}'.format(kwargs['slug_1'], kwargs['slug_2'])
        context['menu_items'] = self.get_menu(kwargs['slug_2'], kwargs['slug_1'])
        context['content_page'] = Publication.objects.filter(tags__contains=kwargs['slug_2']).order_by('-published_date')
        context['cur_page'] = self.cur_page_check()
        context['pages_num'] = self.pages_num(context['content_page'])
        context['content_page'] = self.get_content(context['cur_page'], context['content_page'])
        return context


class RecordView(TemplateView, Helper):
    template_name = "publication.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication'] = Publication.objects.get(slug=kwargs['slug'])
        context['menu_items'] = self.LIBRARY_MENUS['default']
        return context


class AboutView(TemplateView, Helper):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication'] = Publication.objects.get(slug='kontakty')
        context['menu_items'] = self.LIBRARY_MENUS['default']
        return context
