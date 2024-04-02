import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    paid_date = django_filters.DateFromToRangeFilter()
    course = django_filters.CharFilter(field_name='course__name', lookup_expr='icontains')
    lesson = django_filters.CharFilter(field_name='lesson__name', lookup_expr='icontains')
    payment_method = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = ['paid_date', 'course', 'lesson', 'amount', 'payment_method']
