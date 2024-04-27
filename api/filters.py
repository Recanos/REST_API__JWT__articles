# filters.py
from datetime import timedelta

import django_filters
from django.utils import timezone

from .models import Articles


class ArticleFilter(django_filters.FilterSet):
    added = django_filters.ChoiceFilter(choices=[
        ('last_5_minutes', 'Последние 5 минут'),
        ('last_hour', 'Последний час'),
        ('last_day', 'Последние сутки'),
        ('last_week', 'Последняя неделя'),
    ], method='filter_by_time')

    def filter_by_time(self, queryset, name, value):
        if value == 'last_5_minutes':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(minutes=5))
        elif value == 'last_hour':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(hours=1))
        elif value == 'last_day':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=1))
        elif value == 'last_week':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(weeks=1))
        return queryset
    class Meta:
        model = Articles
        fields = []