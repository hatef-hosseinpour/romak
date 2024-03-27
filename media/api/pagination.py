from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q

class CustomEngineroomPagination(PageNumberPagination):
    page_size = 3
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
    
    # def paginate_queryset(self, queryset, request, view=None):
        
    #     installer = request.GET.get('installer')
    #     organization = request.GET.get('organization')
    #     administration = request.GET.get('administration')
    #     province =  request.GET.get('province')
    #     city =  request.GET.get('city')

    #     if installer:
    #         queryset = queryset.filter(creator__username=installer)
    #     if organization:
    #         queryset = queryset.filter(organization=organization)
    #     if administration:
    #         queryset = queryset.filter(administration=administration)
    #     if province:
    #         queryset = queryset.filter(locationpublicinfo__province=province)
    #     if city:
    #         queryset = queryset.filter(locationpublicinfo__city=city)

    #     # queryset = queryset.order_by('id')

    #     return super().paginate_queryset(queryset, request, view)
    


class CustomUserPagination(PageNumberPagination):
    page_size = 5
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
        role = request.GET.get('role')
        status = request.GET.get('status')

        if role == 'superuser':
            queryset = queryset.filter(Q(is_superuser=True) & Q(is_staff=True))
        elif role == 'staff':
            queryset = queryset.filter(Q(is_superuser=False) & Q(is_staff=True))
        elif role == 'installer':
            queryset = queryset.filter(Q(is_superuser=False) & Q(is_staff=False))

        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'deactive':
            queryset = queryset.filter(is_active=False)

        return super().paginate_queryset(queryset, request, view)