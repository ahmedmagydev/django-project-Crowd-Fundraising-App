from django.contrib import messages
import datetime
from django.shortcuts import render, reverse, redirect, HttpResponse, get_object_or_404

# Create your views here.

from projects.models import Project, Image
from comments.models import Comments

from categories.models import Categories
from tags.models import Tags

from accounts.models import UserProfile
from django.db.models import Avg


def home(request):
    approved_projects = Project.get_approved_projects()

    recently_creatd_projects = Project.get_recently_created_projects()
    projs_by_cat,  projs_by_tag = [], []

    categories = Categories.get_categories()
    images = Image.objects.all()
    number_of_registered_ppl = UserProfile.objects.all().count() - 1

    print("------------nums---------------------", number_of_registered_ppl)

    supported_users = UserProfile.objects.all()[:3]

    all_rates = Project.objects.annotate(avg_rate=Avg(
        'project_rate')).order_by("-avg_rate")

    if "category_id" in request.GET:
        category_id = request.GET['category_id']

        category = Categories.get_spesific_category(category_id)
        print("----------------inside query params ---------", category_id,
              '\n', category)

        projs_by_cat = Project.filter_projects_by_category(category)
        print("------projc by cat -----", projs_by_cat)

    if "tag_caption" in request.GET:
        tag_caption = request.GET['tag_caption']

        tag = Tags.get_spesific_tag(tag_caption)
        print("----------------inside query params(tag) ---------", tag_caption,
              '\n', tag)

        projs_by_tag = Project.filter_projects_by_tag(tag)
        print("------projc by cat -----", projs_by_tag)

    return render(request, "home/index.html",
                  context={"recently_creatd_projects": recently_creatd_projects,
                           "categories": categories, "approved_projects": approved_projects,
                           "projs_by_cat": projs_by_cat, "all_rates": all_rates,
                           "images": images, "supported_users": supported_users,
                           "number_of_registered_ppl": number_of_registered_ppl,
                           "projs_by_tag": projs_by_tag
                           })


def notfound(request):
    return render(request, "error/notfound.html")


def becomevolunteer(request):
    return render(request, "becomeVoluenteer.html")


def toggle_approve_project(request, project_id):
    project = Project.get_one_project(project_id)
    is_approved = project.is_approved
    project.is_approved = not is_approved
    project.save()
    msg_state = "you as an admin have {approvedState} this project {proj_name}".format(
        approvedState="disapproved" if is_approved else "approverd",
        proj_name=project
    )
    messages.success(request,  msg_state)
    return redirect(reverse("home") + "#trusted_projects")
