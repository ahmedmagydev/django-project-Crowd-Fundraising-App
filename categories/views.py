from django.shortcuts import render, reverse, redirect, HttpResponse, get_object_or_404


""""
https://github.com/hellopyplane/Star-ratings-with-Django-and-Javascript/blob/main/ratings/templates/ratings/main.html


https://github.com/hellopyplane/Star-ratings-with-Django-and-Javascript/blob/main/ratings/models.py

https://github.com/hellopyplane/Star-ratings-with-Django-and-Javascript


"""
# Create your views here.
from projects.models import Project

from categories.models import Categories


def list_Projects_byCategory(request, category_id):
    category = Categories.get_spesific_category(category_id)
   # lst_projects = Project.filter_projects_by_category(category)
    lst_projects = Project.objects.filter(
        category=category_id).first()
    # order_by("-created_at")
    print("---------jkj---cats", lst_projects)

    return redirect(reverse('home') + f"?category_id={category_id}"
                     + '#projs_by_cat')

# return redirect(reverse('home', kwargs={'project_by_cats': lst_projects if lst_projects else []})
#                     )
