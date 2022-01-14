from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.views.generic import TemplateView, ListView

from mongoengine.queryset.visitor import Q
from .models import NiftyFifty


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        news_listings = NiftyFifty.objects.all()
        context['news_listings'] = news_listings
        return context


class SearchNiftyFiftyPage(ListView):
    template_name = "search.html"
    keyword = ''
    columns = ''
    order = ''

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax() or request.GET.get('q'):
            self.keyword = request.GET.get('q')
        if request.is_ajax() or request.GET.get('c'):
            self.columns = request.GET.get('c')
        if request.is_ajax() or request.GET.get('o'):
            self.order = request.GET.get('o')
        return super(SearchNiftyFiftyPage, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return super(SearchNiftyFiftyPage, self).get_template_names()

    def get_queryset(self):
        '''
        Improvement: use django-haystack and elasticsearch for optimum search functionality
        '''

        news = NiftyFifty.objects.all()
        if self.keyword:
            news = news.filter(
                Q(symbol__icontains=self.keyword))
        if self.columns:
            news = news.only(*self.columns.split(','))
        if self.order:
            news = news.order_by(self.order)
        
        return news

    def get_context_data(self, **kwargs):
        context = super(SearchNiftyFiftyPage, self).get_context_data(**kwargs)
        news_listings = self.get_queryset()
        context['search_result'] = news_listings
        context['keyword'] = self.keyword
        return context
