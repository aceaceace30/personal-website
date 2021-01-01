from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, TemplateView

from .mixins import InformationMixin
from .models import Project, Message, Testimonial


class HomeListView(InformationMixin, ListView):
    template_name = 'portfolio/index.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(InformationMixin, DetailView):
    template_name = 'portfolio/project_details.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_project'] = self.get_object().get_previous_or_next_project('next')
        context['previous_project'] = self.get_object().get_previous_or_next_project('previous')
        return context


class TestimonialUpdateView(UpdateView):
    template_name = 'portfolio/client_comment_form.html'
    model = Testimonial
    fields = ('positive_remarks', 'improvement_remarks')
    slug_field = 'hash_key'
    slug_url_kwarg = 'hash_key'
    success_url = reverse_lazy('thank_you')


class ThankYouView(TemplateView):
    template_name = 'portfolio/client_comment_thankyou.html'


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = Message()
        for key, value in request.POST.items():
            setattr(message, key, value)
        message.save()

        send_mail(
            f'{message.subject} - {message.email}',
            message.message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_ADMIN],
            fail_silently=False
        )

        return HttpResponse('OK')
