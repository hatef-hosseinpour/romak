from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
class CustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100
    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        
        installer = request.GET.get('installer')
        organization = request.GET.get('organization')
        administration = request.GET.get('administration')
        # superuser = request.Get.get('is_superuser')
        # staff = request.Get.get('is_staff')
        # active = request.Get.get('is_active')

        if installer:
            queryset = queryset.filter(creator__username=installer)
        if organization:
            queryset = queryset.filter(organization=organization)
        if administration:
            queryset = queryset.filter(administration=administration)

        # if superuser and staff:
        #     queryset = queryset.filter(Q(is_superuser = superuser) & Q(is_staff = staff))
        # if  not superuser and staff:
        #     queryset = queryset.filter(Q(is_superuser = superuser) & Q(is_staff = staff))
        return super().paginate_queryset(queryset, request, view)