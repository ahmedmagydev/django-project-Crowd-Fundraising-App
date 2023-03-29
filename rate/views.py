from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from projects.models import Project
from .forms import RateForm
# Create your views here.

from rate.models import ReportProject, likes
from django.contrib import messages


def reportProject(request,  project_id):
    project = Project.get_one_project(project_id)
    print("----------replay comment ----------", project)
    newReport = ReportProject(project=project)
    newReport.user = request.user
    newReport.save()
    messages.warning(request, "you've reproted this Project")

    return redirect("singleproject", id=project_id)


def toggle_like(request, project_id):
    project = Project.get_one_project(project_id)
    print("----------replay comment ----------", project)

    user_reaction = likes.get_user_reaction_on_proj(project)
    if user_reaction:
        print("------------------------------")
        isLike = user_reaction.like
        print("toggle_like", isLike)
        user_reaction.like = not isLike
        user_reaction.save()
    else:
        user_reaction = likes(project=project, like=True)
        isLike = True
        # user_reaction.user = request.user
        user_reaction.save()
    print("------------islike ---------------", user_reaction)
    msg_state = "you've {status} this project  {project_title}".format(
        status="disliked" if isLike else "liked", project_title=project.title
    )
    messages.info(request, msg_state)

    return redirect("/")


def toggle_like_project(request, project_id):
    project = Project.get_one_project(project_id)
    print("----------replay comment ----------", project)

    user_reaction = likes.get_user_reaction_on_proj(project)
    if user_reaction:
        print("------------------------------")
        isLike = user_reaction.like
        print("toggle_like", isLike)
        user_reaction.like = not isLike
        user_reaction.save()
    else:
        print("pp[p[]]")
        user_reaction = likes(project=project, like=True)
        isLike = False
       # user_reaction.user = request.user
        user_reaction.save()
    print("------------islike ---------------", user_reaction)
    msg_state = "you've {status} this project  {project_title}".format(
        status="disliked" if isLike else "liked", project_title=project.title
    )
    messages.info(request, msg_state)

    return redirect("singleproject", id=project_id)

def rateproject(request,project_id):
    project = Project.get_one_project(project_id)
    print("----------project  ----------", project)
    if request.method == 'POST':
        rate_form=RateForm(request.POST)
        if rate_form.is_valid():
            print("----------the rate data is valid  ----------", request.POST)
            rate=rate_form.save(commit=False)
            rate.user=request.user
            rate.project=project
            rate.save()
            return redirect("singleproject", id=project_id)
        else:
            print("----------the rate data is invalid  ----------", request.POST)
