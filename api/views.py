from __future__ import absolute_import, division, print_function, unicode_literals

from mongoengine.queryset.visitor import Q

from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework.filters import SearchFilter

from feed.serializer import FeedSerializer
from feed.models import NiftyFifty


class NiftyFiftyViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Contains scraped data from NSE India.
    e.g. http://127.0.0.1:8000/api/nse/?q=TATA&c=symbol,high&o=+high
    Q parameter is used to search for specific stocks,
    C parameter is comma separated(optional) columns whose value to be shown
    O parameter is + ascending / - descending and column name for ordering
    Based on the parameter values stated on the url will scan the mongodb table
    '''
    lookup_field = 'id'
    serializer_class = FeedSerializer
    filter_backends = [SearchFilter]
    columns = ['__all__']

    def get_queryset(self):

        queryset = NiftyFifty.objects.all()
        search_keyword = self.request.query_params.get('q', None)
        self.columns = self.request.query_params.get('c', '__all__').split(',')
        order = self.request.query_params.get('o', None)
        if search_keyword:
            queryset = queryset.filter(
                Q(symbol__icontains=search_keyword))
        if self.columns:
            queryset = queryset.only(*self.columns)
        if order:
            queryset = queryset.order_by(order)

        return queryset

    def list(self, request, *args, **kwargs):
        search_page = self.get_queryset()
        serializer = self.get_serializer(search_page, many=True)
        # serializer.Meta.fields = self.columns
        return Response(serializer.data)
