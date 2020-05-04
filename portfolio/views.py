from django.shortcuts import render
from django.http import HttpResponse

from .models import Portfolio


def homepage(request):

	projects = Portfolio.objects.all()

	template_name = 'portfolio/index.html'
	return render(request, template_name, {'projects': projects})