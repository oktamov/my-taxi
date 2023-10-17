from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class WithTotalPagesCountPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_query_param = "page"
    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            {
                "count": getattr(self.page.paginator, "count", 0),
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
