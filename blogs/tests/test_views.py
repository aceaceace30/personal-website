from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from blogs.models import Blog


class TestViews(TestCase):
    """Test Case for blogs/views.py"""

    def test_blog_list_returns_status_200_and_context(self):
        """
        Asserts that BlogListView is returning status 200 on GET request
        and returns context blog data
        """
        baker.make('Blog', _quantity=5)
        url = reverse('blogs:blog-list')
        response = self.client.get(url)
        blog_list_context = response.context[0]['blogs']
        blogs_qs = Blog.objects.all().values()

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(blog_list_context))

        for idx, blog in enumerate(blogs_qs):
            self.assertEqual(blog['title'], getattr(blog_list_context[idx], 'title'))
            self.assertEqual(blog['content'], getattr(blog_list_context[idx], 'content'))