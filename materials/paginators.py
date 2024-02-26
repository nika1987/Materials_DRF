from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    '''Пагинация, 3 элемента на 1 странице, максимальное кол-во страниц - 100'''
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
