from django.urls import reverse
from rest_framework.test import APILiveServerTestCase


class BlogEndpointsTestCase(APILiveServerTestCase):
    """Test for Blog API endpoints. Break this down to multiple classes or files is the endpoints grows large."""
    fixtures = ['portfolio/fixtures/test_user.json',
                'fixtures/blogs_initial_data.json']

    def test_blog_list(self):
        """Asserts that blog list endpoint is returning correct response"""
        url = reverse('api-blog-list')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(4, response.data['count'])

        # check if each item in results has complete keys
        for item in response.data['results']:
            self.assertEqual({'title', 'slug', 'cover', 'content', 'tags'}, set(item.keys()))

    def test_blog_list_filter(self):
        """Asserts that blog list endpoint is returning correct response with filter"""
        url = reverse('api-blog-list')

        get_params = [
            {'title': '10 Git Commands you use every'},
            {'tags': 'Workout,Python'},
            {'slug': '10-git-commands-you-use-everyday'},
            {'tags': 'Workout'}
        ]

        expected_count = [1, 3, 1, 1]

        for count, get_param in zip(expected_count, get_params):
            response = self.client.get(url, get_param)

            self.assertEqual(200, response.status_code)
            self.assertEqual(count, response.data['count'])
            # check if each item in results has complete keys
            for item in response.data['results']:
                self.assertEqual({'title', 'slug', 'cover', 'content', 'tags'}, set(item.keys()))