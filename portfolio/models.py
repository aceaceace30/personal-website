import os
import uuid

from datetime import date, datetime

from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse


class Project(models.Model):
    COMPANY = 'company'
    FREELANCE = 'freelance'
    PERSONAL = 'personal'

    CLASSIFICATION_CHOICES = (
        (COMPANY, 'Company'),
        (FREELANCE, 'Freelance'),
        (PERSONAL, 'Personal'),
    )

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextField(null=True, blank=True)
    back_end = models.CharField(max_length=255, verbose_name='Back-End Technology')
    front_end = models.CharField(max_length=255, verbose_name='Front-End Technology')
    classification = models.CharField(choices=CLASSIFICATION_CHOICES, max_length=30)
    git_link = models.URLField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    ordering = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse('portfolio:project_details', kwargs={'slug': self.slug})

    @property
    def get_image_cover(self):
        image_cover = self.project_images.filter(is_cover=True).first()
        if not image_cover:
            image_cover = self.project_images.all().first()
        try:
            return image_cover.image.url
        except AttributeError:
            return None

    def next_project(self, as_url_path=True) -> object or str:
        """
        Returns next project object or url path. Defaults as_url_path to true to ease use on
        serializers.ReadOnlyField to also use this method, might be better to default this to false
        if there is a way to pass keyword args on the ReadOnlyField
        :param as_url_path: Boolean to return object or url path
        """
        try:
            project = Project.objects.get(ordering=self.ordering+1)
            if not as_url_path:
                return project
            return settings.DOMAIN_NAME + reverse('api-project-detail', kwargs={'slug': project.slug})
        except Project.DoesNotExist:
            return None

    def previous_project(self, as_url_path=True) -> object or str:
        """
        Returns previous project object or url path. Defaults as_url_path to true to ease use on
        serializers.ReadOnlyField to also use this method, might be better to default this to false
        if there is a way to pass keyword args on the ReadOnlyField
        :param as_url_path: Boolean to return object or url path
        :return:
        """
        try:
            project = Project.objects.get(ordering=self.ordering-1)
            if not as_url_path:
                return project
            return settings.DOMAIN_NAME + reverse('api-project-detail', kwargs={'slug': project.slug})
        except Project.DoesNotExist:
            return None


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='project_images')
    description = models.TextField(null=True, blank=True)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f'{self.project.name} - {self.get_image_name}'

    @property
    def get_image_name(self):
        return os.path.basename(self.image.name)


class About(models.Model):
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_age(birthdate) -> int:
        try:
            birthdate = datetime.strptime(birthdate, '%b %d, %Y')
            today = date.today()
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        except ValueError:
            raise ValueError(f'Invalid birthdate format: {birthdate}. Should be m/dd/yyyy (Ex: Nov 30, 1993)')


class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=150)
    ordering = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name

    @staticmethod
    def get_splitted_skill_set() -> Paginator.page:
        """Splits Skills by 2"""
        skills = Skill.objects.filter(active=True)
        paginator = Paginator(skills, skills.count() / 2)
        return paginator.page(1), paginator.page(2)


class Task(models.Model):
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class JobExperience(models.Model):
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    duration = models.CharField(max_length=150)
    tasks = models.ManyToManyField(Task, through='JobExperienceTask', related_name='job_experiences')
    ordering = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return f'{self.job_title} - {self.company}'


class JobExperienceTask(models.Model):
    job_experience = models.ForeignKey(JobExperience, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.job_experience} | {self.task}'


class Testimonial(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    positive_remarks = models.TextField(null=True, blank=True)
    improvement_remarks = models.TextField(null=True, blank=True, verbose_name='Remarks on what needs to be improve')
    email = models.EmailField()
    platform = models.CharField(max_length=60)
    project_description = models.CharField(max_length=75)
    project_year = models.IntegerField(null=True, blank=True)

    hash_key = models.UUIDField(default=uuid.uuid4, editable=False)
    is_answered = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email} - {self.platform}'

    @property
    def link(self) -> str:
        """Returns URL to client comment form. Example: http://test.com/client-comment-form/ad23-qwe1/"""
        path = reverse('client_comment_form', kwargs={'hash_key': str(self.hash_key)})
        return settings.DOMAIN_NAME + path

    def save(self, **kwargs):
        """Override save method to send email on initial creation"""
        if not self.pk:
            subject = 'Request for feedback'
            message = render_to_string('email_templates/testimonial_message.html', context={'testimonial': self})
            try:
                send_mail(
                    subject,
                    '',
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    html_message=message,
                    fail_silently=False
                )
            except:
                pass
        super().save(**kwargs)


class Message(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} - {self.subject}'
