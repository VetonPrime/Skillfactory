from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput


class NewsFilter(FilterSet):

    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='по названию')

    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='по имени автора')

    date_create = DateFilter(
        field_name='date_create',
        lookup_expr='date__gte',
        label='позже указываемой даты',
        widget=DateInput(attrs={'type': 'date'}))

