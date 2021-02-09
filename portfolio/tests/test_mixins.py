from django.conf import settings
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.views.generic import TemplateView

from portfolio.mixins import InformationMixin
from portfolio.models import About, JobExperience, Testimonial


class TestMixin(TestCase):
    """Test case for mixins.py"""

    fixtures = ['portfolio/fixtures/test_mixins.json']

    class TestView(InformationMixin, TemplateView):
        template_name = 'portfolio/index.html'

    def test_information_mixin(self):
        """
        Asserts the information_mixin adds data to context
        :return:
        """
        url = reverse('homepage')
        request = RequestFactory().get(url)

        view = self.TestView()
        view.setup(request)

        context = view.get_context_data()

        info = {
            'birthdate': 'Nov 30, 1993',
            'full_name': 'Michael Ababao',
            'job_title': 'Web Developer / Freelancer',
            'age': About.get_age('Nov 30, 1993'),
        }

        self.assertEqual(info, context['info'])
        self.assertEqual(JobExperience.objects.filter(job_title='PROGRAMMER')[0].job_title,
                         context['job_experiences'][0].job_title)
        self.assertEqual(Testimonial.objects.get(hash_key='10722bf8-8a81-4e2c-8bf6-9836006052ec').name,
                         context['testimonials'][0].name)
