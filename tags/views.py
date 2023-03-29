from tags.models import Tags
from django.shortcuts import render, reverse, redirect, HttpResponse, get_object_or_404

# Create your views here.

from projects.models import Project


def filter_Projects_by_tag(request, tag):
    # tags = Tags.get_spesific_tag(tag)
    # print("---------------TAGS-------------------------", tags, tag)

    # res = Project.objects.filter(tags__in=tags)

    # print("--------------------RES Based on Tags-------------------", '\n',
    #       res)

    return redirect(reverse('home') + f"?tag_caption={tag}"
                    + '#projects_by_tags')
