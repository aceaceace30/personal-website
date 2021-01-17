from django.urls import reverse
from rest_framework.test import APILiveServerTestCase

from model_bakery import baker


class APIEndpointsTestCase(APILiveServerTestCase):
    """Tests for API endpoints. Break this down to separate classes or files if the endpoints grows large"""

    def test_about_endpoint(self):
        """Asserts that plain about endpoint is working"""
        abouts = baker.make('About', 15)
        url = reverse('api:about-list')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.data['results']))  # check if pagination is working

        for idx, about in enumerate(response.data['results']):  # check if values are the same
            self.assertEqual(abouts[idx].name, about['name'])
            self.assertEqual(abouts[idx].value, about['value'])

    def test_about_endpoint_ordering(self):
        """Asserts that about endpoint ordering is working"""
        abouts = baker.make('About', 10)
        url = reverse('api:about-list') + '?ordering=-id'
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # checks if ordering on pk is working by checking the values of first and last item of the result
        self.assertEqual(abouts[-1].pk, response.data['results'][0]['pk'])
        self.assertEqual(abouts[0].pk, response.data['results'][-1]['pk'])

    def test_about_endpoint_field_filtering(self):
        """Asserts that about endpoint field filtering is working"""
        abouts = baker.make('About', 5)
        about = abouts[0]
        url = reverse('api:about-list') + f'?name={about.name}&value={about.value}'
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['count'])  # check if it filters out data
        self.assertEqual(about.name, response.data['results'][0]['name'])
        self.assertEqual(about.value, response.data['results'][0]['value'])

    def test_project_endpoint(self):
        """Todo: Add test for project endpoint"""

    def test_project_detail_endpoint(self):
        """Todo: Add test for project detail endpoint"""

    def test_skill_endpoint(self):
        """Todo: Add test for skill endpoint"""

    def test_job_experience_endpoint(self):
        """Todo: Add test for about endpoint"""

    def test_testimonial_endpoint(self):
        """Todo: Add test for testimonial endpoint"""