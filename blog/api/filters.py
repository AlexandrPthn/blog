from django_filters.rest_framework import CharFilter, DateFilter, FilterSet

from .models import Blog, Post


class BlogFilter(FilterSet):
    start_date = DateFilter(field_name="updated_at", lookup_expr='gte')
    end_date = DateFilter(field_name="updated_at", lookup_expr='lte')

    class Meta:
        model = Blog
        fields = '__all__'


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='istartswith')
    start_date = DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Post
        fields = '__all__'
