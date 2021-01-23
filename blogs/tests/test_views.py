from django.test import TestCase
from django.urls import reverse

from blogs.models import Blog


class TestViews(TestCase):
    """Test Case for blogs/views.py"""

    fixtures = ['blogs/fixtures/test_views.json']

    def test_blog_list_returns_status_200_and_context(self):
        """
        Asserts that BlogListView is returning status 200 on GET request
        and returns context blog data
        """
        url = reverse('blogs:blog-list')
        response = self.client.get(url)
        blog_list_context = response.context[0]['blogs']
        blogs_qs = Blog.objects.filter(active=True).values()

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(blog_list_context))

        for idx, blog in enumerate(blogs_qs):
            self.assertEqual(blog['title'], getattr(blog_list_context[idx], 'title'))
            self.assertEqual(blog['slug'], getattr(blog_list_context[idx], 'slug'))
            self.assertEqual(blog['content'], getattr(blog_list_context[idx], 'content'))

    def test_blog_detail_returns_status_200_and_context(self):
        """
        Asserts that BlogDetailView is returning status 200 on GET request
        and returns context blog data
        """
        blog = Blog.objects.get(slug='my-second-blog')
        url = reverse('blogs:blog-detail', kwargs={'slug': blog.slug})
        response = self.client.get(url)
        blog_context = response.context[0]['blog']

        self.assertEqual(200, response.status_code)
        self.assertEqual(blog.title, getattr(blog_context, 'title'))
        self.assertEqual(blog.slug, getattr(blog_context, 'slug'))
        self.assertEqual(blog.content, getattr(blog_context, 'content'))

    def test_blog_detail_returns_status_400(self):
        """Asserts that BlogDetailView is returning status 404 for GET request with inactive/not existing slug"""

        # for inactive blog
        url = reverse('blogs:blog-detail', kwargs={'slug': 'my-inactive-blog'})
        response1 = self.client.get(url)

        self.assertEqual(404, response1.status_code)

        # for not existing blog
        url = reverse('blogs:blog-detail', kwargs={'slug': 'not-existing-blog'})
        response1 = self.client.get(url)

        self.assertEqual(404, response1.status_code)