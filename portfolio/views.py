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
	
	if not next_project:
		next_project = None
	else:
		next_project = next_project[0]

	return render(request, template_name, {'project': project, 'next_project': next_project})