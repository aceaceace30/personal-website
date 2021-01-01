from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from portfolio.models import Message, Testimonial


class TestViews(TestCase):
    """Test case for views.py"""

    fixtures = ['test_views.json']

    def test_home_list_view_status_200(self):
        """
        Asserts that home page is working
        :return:
        """
        url = reverse('portfolio:homepage')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_project_detail_view_status_200(self):
        """
        Asserts that project_detail page is working
        :return:
        """
        slug_list = ['qoute-generator', 'inventory-management-system']

        for slug in slug_list:
            url = reverse('portfolio:project_details', kwargs={'slug': slug})
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_project_detail_view_status_404(self):
        """
        Asserts that project_detail returns 404 if project does not exist
        :return:
        """
        url = reverse('portfolio:project_details', kwargs={'slug': 'test-project'})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_thankyou_view_status_200(self):
        """
        Asserts that thank you page is working
        :return:
        """
        url = reverse('thank_you')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_send_message(self):
        """
        Asserts that send_message is working properly
        - returns status 200
        - returns OK HttpResponse
        - saves value to db
        - send_mail function is being called
        :return:
        """
        url = reverse('portfolio:send_message')
        data = {
            'name': 'test_name',
            'email': 'test@test.com',
            'subject': 'test_subject',
            'message': 'test_message',
        }

        with patch('portfolio.views.send_mail') as mock_send_mail:
            response = self.client.post(url, data=data)
            self.assertEqual(200, response.status_code)
            self.assertEqual(b'OK', response.content)
            self.assertTrue(Message.objects.filter(name='test_name').exists())
            self.assertTrue(mock_send_mail.called)

    def test_testimonial_update_view_status_200(self):
        """
        Asserts that TestimonialUpdateView returns status 200
        :return:
        """
        url = reverse('client_comment_form', kwargs={'hash_key': '10722bf8-8a81-4e2c-8bf6-9836006052ec'})
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_testimonial_update_view_post(self):
        """
        Asserts that TestimonialUpdateView is working properly
        - positive_remarks, improvement_remarks has been updated
        - is_answered field is set to True
        - Permission Denied is raised after the update has been saved
        :return: 
        """
        hash_key = '10722bf8-8a81-4e2c-8bf6-9836006052ec'
        url = reverse('client_comment_form', kwargs={'hash_key': hash_key})
        data = {
            'positive_remarks': 'Test Positive Remarks',
            'improvement_remarks': 'Test Improvement Remarks',
        }
        self.client.post(url, data=data)

        testimonial = Testimonial.objects.get(hash_key=hash_key)
        self.assertEqual('Test Positive Remarks', testimonial.positive_remarks)
        self.assertEqual('Test Improvement Remarks', testimonial.improvement_remarks)
        self.assertTrue(testimonial.is_answered)

        response = self.client.get(url)
        self.assertEqual(302, response.status_code)