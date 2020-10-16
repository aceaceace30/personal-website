from django.test import TestCase
from portfolio.models import Project, About


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