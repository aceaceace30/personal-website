from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Portfolio


def homepage(request):

	projects = Portfolio.objects.all()

	template_name = 'portfolio/index.html'
	return render(request, template_name, {'projects': projects})

def detail(request, name):
	project = get_object_or_404(Portfolio, slug=name)
	template_name = 'portfolio/detail.html'
	next_project = Portfolio.objects.exclude(pk__lte=project.pk).order_by('id')
	previous_project = None
	if project.pk != 1:
		previous_project = Portfolio.objects.get(pk=(project.pk-1))
	
	if not next_project:
		next_project = None
	else:
		next_project = next_project[0]

	context = {
		'project': project,
		'next_project': next_project,
		'previous_project': previous_project
	}

	return render(request, template_name, context)