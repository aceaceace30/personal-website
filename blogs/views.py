from django.views.generic import TemplateView


class BlogListView(TemplateView):
    template_name = 'blogs/blog_list.html'
