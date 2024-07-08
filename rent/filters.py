from django_filters import rest_framework as filter
from .models import Advertisement


class AdvertisementFilter(filter.FilterSet):
    keyword = filter.CharFilter(field_name="title", lookup_expr="icontains")
    min_price = filter.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filter.NumberFilter(field_name="price", lookup_expr="lte")
    order_by = filter.OrderingFilter(
        fields=(('price', 'price'), ('rating', 'rating'))
    )

    class Meta:
        model = Advertisement
        fields = ('category', 'division', 'district',)
