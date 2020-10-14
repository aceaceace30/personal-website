from django.views.generic import ListView, DetailView

from .mixins import InformationMixin
from .models import Project


class HomeListView(InformationMixin, ListView):
	template_name = 'portfolio/index.html'
	model = Project
	context_object_name = 'projects'


class ProjectDetailView(DetailView):
	template_name = 'portfolio/project_details.html'
	model = Project
	context_object_name = 'project'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['next_project'] = self.get_object().get_previous_or_next_project('n')
		context['previous_project'] = self.get_object().get_previous_or_next_project('p')
		return context