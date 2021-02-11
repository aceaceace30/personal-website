import django_filters

from blogs.models import Blog


class Many2ManyFilter(django_filters.Filter):
    """
    Customized filter to support filtering with `,` on many to many fields.
    Eg: https://test.com/?tags=Python,Django
    """
    def filter(self, qs, value):
        if not value:
            return qs

        if ',' in value:
            values = value.split(',')
        else:
            values = [value]

        lookup = f'{self.field_name}__{self.lookup_expr}'
        return qs.filter(**{lookup: values})


class BlogFilter(django_filters.FilterSet):
    tags = Many2ManyFilter(field_name='tags__name', lookup_expr='in')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ('title', 'slug', 'tags',)