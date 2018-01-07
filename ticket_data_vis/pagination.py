from rest_framework.pagination import LimitOffsetPagination

class TicketsOffsetPagination(LimitOffsetPagination):
    max_limit = 100
