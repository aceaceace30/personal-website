from django.views.generic import ListView

from blogs.models import Blog


class BlogListView(ListView):
    template_name = 'blogs/blog_list.html'
    model = Blog
    context_object_name = 'blogs'
    queryset = Blog.objects.filter(active=True)
