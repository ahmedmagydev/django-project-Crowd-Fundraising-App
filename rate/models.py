from accounts.models import UserProfile
from django.db import models
from projects.models import Project
from django_enum import EnumField

# Create your models here.

# if -> request.user._is_superuser
"""
{% if not request.user.is_superuser %}

"""
from django.db.models import Avg


class Rating(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_rating")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_rate")

    rate = models.DecimalField(max_digits=5, decimal_places=2)

    @classmethod
    def get_project_avg_rate(cls, project):
        rate_lst = cls.objects.filter(
            project=project)

        avg = round(rate_lst.aggregate(Avg("rate"))[
                    "rate__avg"], 2) if rate_lst else 0
        return avg


class ReportOption(models.TextChoices):
    VALUE0 = 'V0', 'in'
    VALUE1 = 'V1', 'Value 1'
    VALUE2 = 'V2', 'Value 2'


class ReportProject(models.Model):

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_reaction")

    project = models.ForeignKey(
        Project, related_name="report_project", on_delete=models.CASCADE)
    # user = models.ForeignKey(User, related_name="user_report")
    option = EnumField(ReportOption, null=True, blank=True)

# register like in admin ->>>>


class likes(models.Model):
    # user = models.ForeignKey(
    #     UserProfile, on_delete=models.CASCADE, related_name="user_reaction")

    like = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project, related_name="like_project", on_delete=models.CASCADE)

    def __str__(self):
        return "liked" if self.like else "not like"

    @classmethod
    def get_project_likes_number(cls, project):
        return cls.objects.filter(project=project, like=True).count()

    @classmethod
    def get_project_likes(cls, project):
        return cls.objects.filter(project=project, like=False).count()

    @classmethod
    def get_user_reaction_on_proj(cls, project, user='user'):
        return cls.objects.filter(project=project).first()  # , user=user)
