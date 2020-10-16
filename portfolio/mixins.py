from django.conf import settings

from portfolio.models import About, Skill, JobExperience


class InformationMixin:
    """
    Adds needed information to context data
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_path'] = settings.RESUME_PATH
        try:
            context = self.add_info(context)
            context = self.add_skills(context)
            context = self.add_job_experience(context)
        except KeyError:
            pass
        return context

    @staticmethod
    def add_info(context):
        info = {about.name: about.value for about in About.objects.all()}
        info['age'] = About.get_age(info['birthdate'])
        context['info'] = info
        return context

    @staticmethod
    def add_skills(context):
        skill_set1, skill_set2 = Skill.get_splitted_skill_set()
        context['skill_set1'] = skill_set1
        context['skill_set2'] = skill_set2
        return context

    @staticmethod
    def add_job_experience(context):
        context['job_experiences'] = JobExperience.objects.filter(active=True)
        return context
