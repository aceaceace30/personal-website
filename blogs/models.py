from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(max_length=75, unique=True)
    color = ColorField(unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = RichTextField()
    tags = models.ManyToManyField(Tag, through='BlogTag')

    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_blogs', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_blogs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        default_related_name = 'blogs'

    def __str__(self):
        return self.title


class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.blog.title} - {self.tag.name}'
