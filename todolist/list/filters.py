import django_filters
from .models import *


class DeskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="Desk's name", lookup_expr='icontains')

    class Meta:
        model = Desk
        fields = ['name']
