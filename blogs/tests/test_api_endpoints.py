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
        self.assertEqual(3, response.data['count'])

        # TODO: Added assertion to check if the fields being retrieve is complete