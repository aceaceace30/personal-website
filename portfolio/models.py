from django.db import models
from django.urls import reverse

class Portfolio(models.Model):

	CLASSIFICATION_CHOICES = (
		('', '----'),
		('company', 'Company'),
		('freelance', 'Freelance'),
		('personal', 'Personal'),
		)

	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	description = models.TextField(max_length=255, null=True, blank=True)
	back_end = models.CharField(max_length=255)
	front_end = models.CharField(max_length=255)
	classification = models.CharField(choices=CLASSIFICATION_CHOICES, max_length=30)
	cover = models.ImageField(null=True, blank=True, upload_to='portfolio_images/')
	git_link = models.URLField(null=True, blank=True)
	website_link = models.URLField(null=True, blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('portfolio:detail', kwargs={'slug':self.slug})