import django_filters
from .models import *

class LeaveFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date_from')
    till_date = django_filters.DateFilter(field_name='till_date')
    students_left = django_filters.DateRangeFilter(field_name='date_from')
    students_returned = django_filters.DateRangeFilter(field_name='till_date')

    class Meta():
        model = Applications
        fields = ['date_from', 'till_date', ]
