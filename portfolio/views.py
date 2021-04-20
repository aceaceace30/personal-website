from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, TemplateView

from .decorators import check_if_testimonial_is_answered
from .mixins import InformationMixin
from .models import Project, Message, Testimonial
from .tasks import send_mail_task


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
        context['next_project'] = self.get_object().next_project(as_url_path=False)
        context['previous_project'] = self.get_object().previous_project(as_url_path=False)
        return context


@method_decorator(check_if_testimonial_is_answered, name='dispatch')
class TestimonialUpdateView(UpdateView):
    template_name = 'portfolio/client_comment_form.html'
    model = Testimonial
    fields = ('positive_remarks', 'improvement_remarks')
    slug_field = 'hash_key'
    slug_url_kwarg = 'hash_key'
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        """Override form_valid to update the is_answered field"""
        self.object = form.save(commit=False)
        self.object.is_answered = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ThankYouView(TemplateView):
    template_name = 'portfolio/client_comment_thankyou.html'


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = Message()
        for key, value in request.POST.items():
            setattr(message, key, value)
        message.save()

        send_mail_task(message.subject, message.email, message.message)

        return HttpResponse('OK')
