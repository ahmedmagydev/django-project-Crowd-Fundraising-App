

from projects.models import Project
from accounts.models import UserProfile
from comments.models import Comments

from rate.models import likes

from django import template

register = template.Library()


@register.simple_tag
def get_method(project):
    return Comments.get_project_number_of_comments(project)


@register.simple_tag
def get_project_total_reactions(project):
    total_reactions = likes.get_project_likes_number(project)
    return total_reactions if total_reactions else 0


@register.simple_tag
def recently_created_projects():
    return Project.get_recently_created_projects()


@register.simple_tag
def get_user_info(user):
    user_account = UserProfile.objects.filter(username=user).first()
    print("------USER----------", user_account)
    return user_account


@register.simple_tag
def get_user_react_on_project(project):
    queries = likes.get_user_reaction_on_proj(project)
    return queries.like if queries else False
