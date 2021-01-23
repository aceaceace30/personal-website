import os

from ckeditor_uploader.fields import RichTextUploadingField
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
    cover = models.ImageField(upload_to='blog_covers', null=True, blank=True)
    content = RichTextUploadingField()
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

    @property
    def cover_name(self):
        return os.path.basename(self.cover.url)


class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'blog_tags'
        unique_together = ('blog', 'tag')

    def __str__(self):
        return self.tag.name

    @property
    def color(self):
        return self.tag.color

    @property
    def name(self):
        return self.tag.name
