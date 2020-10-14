from django.contrib import admin
from .models import Project, About, Skill, Task, JobExperience


class TaskInline(admin.TabularInline):
    model = JobExperience.task.through


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_filter = ('classification', 'created_at')
    search_fields = ('name', 'slug')
    list_display = ('name', 'slug', 'ordering', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):

    search_fields = ('name', 'value')
    list_display = ('name', 'value', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    search_fields = ('name', 'value')
    list_display = ('name', 'value', 'ordering', 'active', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    search_fields = ('description',)
    list_display = ('description', 'active', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    inlines = (TaskInline, )
    search_fields = ('job_name', 'job_title')
    list_display = ('job_title', 'company', 'ordering', 'active', 'created_at')
    readonly_fields = ('created_at',)
