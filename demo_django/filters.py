from demo_django.models import Food, Category, Type
from demo_drf.models import Offer
from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter
from django.forms.widgets import TextInput
from django.db.models import Q


class MenuFilter(FilterSet):
    """
    Menu filter
    """
    search = CharFilter(method='custom_filter', widget=TextInput(attrs={'placeholder': 'Search'}),
                        label='')

    class Meta:
        model = Food
        fields = ['search']

    def custom_filter(self, queryset, name, value):
        """
        Custom search filter
        """
        value = value.split('?')[0]
        return queryset.filter(
            Q(name__icontains=value) |
            Q(items__icontains=value) |
            Q(types__name__icontains=value) |
            Q(categorys__name__icontains=value)
        ).distinct()
