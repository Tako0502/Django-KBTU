import django_filters
from .models import Expense, Category

class ExpenseFilter(django_filters.FilterSet):
    # Filter for a date range
    date = django_filters.DateFromToRangeFilter()
    # Filter by category
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.none())

    class Meta:
        model = Expense
        fields = ['date', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.filters['category'].queryset = Category.objects.filter(user=user)
