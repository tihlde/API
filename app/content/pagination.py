from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

from rest_framework.utils.urls import remove_query_param, replace_query_param


class BasePagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "None"


    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_page()),
            ('previous', self.get_previou_page()),
            ('results', data)
        ]))

    def get_next_page(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()
    
    def get_previou_page(self):
        if not self.page.has_previous() or self.page.previous_page_number() < 1:
            return None
        return self.page.previous_page_number()
        

    


    
