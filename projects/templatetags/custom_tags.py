

from tags.models import Tags
from accounts.models import UserProfile
from comments.models import Comments
from projects.models import Image, Project

from rate.models import likes

from django import template

register = template.Library()


@register.simple_tag
def get_method(project):
    return Comments.get_project_number_of_comments(project)


# #  <img
#                          src="{% static 'images/blog/comment-one-img1.jpg' %}"
#                          alt="#" />


@register.simple_tag
def get_user_image(user):
    user_account = UserProfile.objects.filter(user=user).first()
    print("------USER----------", user_account, user_account.photo)
    return user_account.photo


@register.simple_tag
def get_user_react_on_project(project, user=''):
    queries = likes.get_user_reaction_on_proj(project)
    return queries.like if queries else False


@register.simple_tag
def get_project_images(project):
    queries = Image.objects.filter(project=project)
    return queries.image if queries else False


@register.simple_tag
def get_projects_with_similar_tags(project):

    tag_caption = project.tags.all
    print("---------------TAGS-------------------------",
          [tag for tag in project.tags.all()])
    # tags
    tag = Tags.get_spesific_tag(tag_caption)
    print("----------------inside query params(tag) ---------", tag_caption,
          '\n', tag)

    projs_by_tag = Project.filter_projects_by_tag(tag)
    print("------projc by cat -----", projs_by_tag)
