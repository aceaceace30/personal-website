from django.urls import reverse
from rest_framework.test import APILiveServerTestCase

from model_bakery import baker

from portfolio.models import Project


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
        """Asserts that plain project endpoint is working"""
        baker.make('Project', 20)

        url = reverse('api:project-list')
        response = self.client.get(url)
        result = response.data['results']

        fields_to_check = ['name', 'slug', 'description', 'back_end', 'front_end',
                           'classification', 'git_link', 'website_link', 'ordering']

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(result))  # check if pagination is working

        # check if all retrieved values are the same
        project_qs = Project.objects.all().values()[:10]

        for idx, project in enumerate(project_qs):
            for field in fields_to_check:
                self.assertEqual(project[field], result[idx][field])

    def test_project_endpoint_ordering(self):
        """Asserts that project endpoint with ordering is working"""
        baker.make('Project', 10)

        order_fields = ['-ordering', 'name', '-slug', 'classification']
        fields_to_check = ['name', 'slug', 'description', 'back_end', 'front_end',
                           'classification', 'git_link', 'website_link', 'ordering']

        for order_field in order_fields:
            url = reverse('api:project-list') + f'?ordering={order_field}'
            response = self.client.get(url)
            result = response.data['results']

            self.assertEqual(200, response.status_code)

            # check if all retrieved values are the same
            project_qs = Project.objects.order_by(order_field).values()
            for idx, project in enumerate(project_qs):
                for field in fields_to_check:
                    self.assertEqual(project[field], result[idx][field])

    def test_project_endpoint_filtering(self):
        """Asserts that project endpoint with filtering is working"""
        baker.make('Project', 15)
        project_company_count = Project.objects.filter(classification='company').count()
        url = reverse('api:project-list') + '?classification=company'
        response = self.client.get(url)

        result_project_company_count = 0
        for result in response.data['results']:
            if result['classification'] == 'company':
                result_project_company_count += 1

        self.assertEqual(200, response.status_code)
        self.assertEqual(project_company_count, result_project_company_count)

    def test_project_detail_endpoint(self):
        """Todo: Add test for project detail endpoint"""

    def test_skill_endpoint(self):
        """Todo: Add test for skill endpoint"""

    def test_job_experience_endpoint(self):
        """Todo: Add test for about endpoint"""

    def test_testimonial_endpoint(self):
        """Todo: Add test for testimonial endpoint"""
