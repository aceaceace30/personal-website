import os
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from portfolio.models import Project, Testimonial


class TestProjectModel(TestCase):
    """Test for methods of Project model"""

    fixtures = ['portfolio/fixtures/test_models.json']

    def test_get_image_cover(self):
        """
        Test get_image_cover method returns correct path
        :return:
        """
        project = Project.objects.get(slug='recruitment-system')
        self.assertEqual('/media/test_path/test_image1.png', project.get_image_cover)

    def test_get_previous_or_next_project(self):
        """
        Test get_previous_or_next_project method returns
        previous or next project
        :return:
        """
        project1 = Project.objects.get(slug='recruitment-system')
        project2 = Project.objects.get(slug='document-management')
        project3 = Project.objects.get(slug='daily-task')

        self.assertEqual(project2, project1.get_previous_or_next_project('next'))
        self.assertEqual(project2, project3.get_previous_or_next_project('previous'))
        self.assertIsNone(project1.get_previous_or_next_project('previous'))

    def test_link_property(self):
        """
        Test link method returns correct url
        :return:
        """
        hash_key = '10722bf8-8a81-4e2c-8bf6-9836006052ec'
        testimonial = Testimonial.objects.get(hash_key=hash_key)
        path = reverse('client_comment_form', kwargs={'hash_key': hash_key})
        expected_url = os.path.join(settings.DOMAIN_NAME, path)

        self.assertEqual(expected_url, testimonial.link)

    def test_testimonial_save(self):
        """
        Test creation of testimonial calls send_mail and updating does not
        :return:
        """
        with patch('portfolio.models.send_mail') as patch_send_mail:
            testimonial = Testimonial()
            testimonial.name = 'Test Name'
            testimonial.email = 'test@email.com'
            testimonial.platform = 'test platform'
            testimonial.project_description = 'new project'
            testimonial.active = True
            testimonial.save()
            patch_send_mail.assert_called_once()

        with patch('portfolio.models.send_mail') as patch_send_mail:
            testimonial = Testimonial.objects.get(email='test@email.com')
            testimonial.positive_remarks = 'Test Positive Remarks'
            testimonial.save()
            patch_send_mail.assert_not_called()
