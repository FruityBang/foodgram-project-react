from rest_framework.pagination import PageNumberPagination

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
