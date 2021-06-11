from rest_framework.pagination import LimitOffsetPagination

# this will set the max limit when the parameter is set by user
class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # set the maximum limit value to 8
    max_limit = 8
