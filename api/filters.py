
from django_filters import rest_framework as filters


from .models import Document


class DateFilter(filters.FilterSet):
    '''filter for by created at filed'''
    created_at_gte = filters.DateFilter(field_name="created_at",
                                        lookup_expr='gte')
    created_at_lte = filters.DateFilter(field_name="created_at",
                                        lookup_expr='lte')
    created_at = filters.DateFilter(field_name="created_at",
                                    lookup_expr='contains')

    class Meta:
        model = Document
        fields = ['created_at_gte', "created_at_lte", "created_at"]
