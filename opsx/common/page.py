import math
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data),
            ('total_pages', self.get_total_pages()),
            ('page', self.get_current_page()),
        ]))

    def get_current_page(self):
        return self.page.next_page_number() - 1

    def get_total_pages(self):
        return math.floor(self.page.paginator.count / self.page_size)

    page_size = 15
    page_size_query_param = 'limit'
    max_page_size = 1000


class GlobalPage(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.get_current_page()),
            ('total_pages', math.floor(self.page.paginator.count / self.page_size)),
            ('results', data)
        ]))

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                page_size = _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
                self.page_size = page_size
                return page_size
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_current_page(self):
        if not self.page.has_next():
            return 0
        page_number = self.page.next_page_number() - 1
        return page_number

    page_size = 15
    page_size_query_param = 'limit'
    max_page_size = 999999


class Page():
    pagination_class = StandardResultsSetPagination
