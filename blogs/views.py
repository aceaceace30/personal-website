from django.views.generic import ListView, DetailView

from blogs.models import Blog


class BlogListView(ListView):
    template_name = 'blogs/blog_list.html'
    model = Blog
    context_object_name = 'blogs'
    queryset = Blog.objects.filter(active=True)


class BlogDetailView(DetailView):
    template_name = 'blogs/blog_detail.html'
    model = Blog
    context_object_name = 'blog'
