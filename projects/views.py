from django.db.models import Sum, Avg, Count
from tags.models import Tags
from re import sub
from decimal import Decimal
from comments.forms import CommentForm
from rate.forms import RateForm
from projects.models import Project, Donate, Image
from rate.models import Rating
from .donation_forms import DonationForm
from django.contrib.auth.decorators import login_required
from .forms import NewProjectForm
from comments.models import Comments, Reply
from django.shortcuts import render, reverse, redirect, HttpResponse, get_object_or_404
from .donation_forms import DonationForm
from .forms import NewProjectForm, Project_Image_Form
from django.core.files.storage import FileSystemStorage
# Create your views here.
from djmoney.money import Money
from django.db.models import Q


# get_project_comments


from django.contrib import messages


def donation(request):
    return render(request, "projects/index.html")


@login_required
def submitDonation_dup(request, id):
    # spesify on which project donation would be send
    project = Project.get_one_project(id)

    if request.method == "POST":
        donationForm = DonationForm(request.POST)
        donation.user = request.user
        if donationForm.is_valid():
            print(donationForm.cleaned_data["donation"])
            print("-----------------", project.total_donation)

            project.total_donation += Money(
                donationForm.cleaned_data["donation"], 'USD')
            print("-----------------", project.total_donation)
            project.save()
        # show donation upgrade
    else:
        donationForm = donationForm()

    return redirect("singleproject", id=id)


def submitDonation(request, id):
    # spesify on which project donation would be send
    project, amount = Project.get_one_project(id), 0

    if "amount" in request.GET:
        amount = request.GET['amount']

    if request.method == "POST":
        donationForm = DonationForm(request.POST)

        if donationForm.is_valid():
            amount = Money(
                donationForm.cleaned_data["donation"], 'USD') if not amount else Money(amount)

            # print(donationForm.cleaned_data["donation"])
            print("-----------------", amount)

            # project.total_donation += Money(
            #     donationForm.cleaned_data["donation"], 'USD')
            # print("-----------------", project.total_donation)
        # show donation upgrade
        else:
            donationForm = donationForm()

    newdonation = Donate(project=project, amount_of_donation=amount)
    newdonation.user = request.user
    print("--------------newdonation---", newdonation)
    # newdonation.amount_of_donation = Money(
    #     donationForm.cleaned_data["donation"], 'USD')

    messages.success(request, "donation sumbited sussesfully")
    newdonation.save()

    return redirect("singleproject", id=id)


def donationlist(request):
    return render(request, "projects/listDonation.html")


def singledonation(request, id):
    project = Project.get_one_project(id)
    project_comments = Comments.get_project_comments(project)
    images = Image.objects.all()
    # project_replys = Reply.get_comment_replys(project_comments)
    replys = Reply.get_project_replys(project)
    # calcualations
    project_comments_number = Comments.get_project_number_of_comments(project)
    project_total_donation = Donate.get_total_donation_for_project(project)

    # forms
    donationForm = DonationForm()
    commentForm = CommentForm()
    replyForm = CommentForm()

    tags = project.tags.all()

    # tags = project.tags.values_list('caption', flat=True)
    print("---------------TAGS-------------------------", tags)

    res = Project.objects.filter(tags__in=tags).exclude(id=id)
    similar_projects = res.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-created_at')

    print("------RES-------", res)
    # rating
    rated_before = Rating.objects.filter(
        user=request.user, project=project).exists()
    if rated_before:
        rateForm = None
        user_rate_to_show = Rating.objects.filter(
            user=request.user, project=project).first().rate

    else:
        user_rate_to_show = None
        rateForm = RateForm()
    images = Image.objects.all()

    # print("---------donation total----------------------", project_total_donation)

    avg_rate = Rating.get_project_avg_rate(project)

    # print("----avg_rate-------", avg_rate)
    return render(request, "projects/projectdetail.html",
                  context={"donationForm": donationForm, "project": project,
                           "replyForm": replyForm, "avg_rate": avg_rate,
                           # "comments_replys": comments_replys,
                           "replys": replys, 'images': images,
                           "similar_projects": similar_projects,
                           "project_comments_number": project_comments_number,
                           "project_total_donation": project_total_donation if project_total_donation else 0,
                           "commentForm": commentForm, "project_comments": project_comments, "rateForm": rateForm, 'user_rate_to_show': user_rate_to_show
                           })


def newdonation(request):
    return render(request, "projects/newproject.html")


# ahmed ->

def single_project_view(request, id):
    project = Project.get_one_project(id)

    return


def projectslist(request):
    query = request.GET.get('query', '')
    projects = Project.get_projects()

    all_rates = Project.objects.annotate(avg_rate=Avg(
        'project_rate')).order_by("-avg_rate")

    for rate in all_rates:
        print("--------opo---", rate)

    images = Image.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(details__icontains=query))
    images = Image.objects.all()

    return render(request, "projects/listProjects.html/",
                  {'projects': projects, 'images': images, 'query': query})


# @login_required
def newproject(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            print("------------USER------------------------------", request.user)
            # Get the form data from the POST request
            project_form = NewProjectForm(request.POST)
            image_form = Project_Image_Form(request.POST, request.FILES)

            print(request.FILES)
            print("------------type--------------", type(request.user))

            if project_form.is_valid():
                # Create a new Project object with the form data
                project = project_form.save(commit=False)
                project.user = request.user
                project.save()
                # Get the uploaded images and create an Image object for each one
                for image in request.FILES.keys():
                    image_file = request.FILES.getlist(image)
                    for i in image_file:
                        fs = FileSystemStorage()
                        filename = fs.save('images/projects/' + i.name, i)
                        img = Image()
                        img.image = filename
                        img.project = project
                        img.save()

                # Redirect to the detail view of the new project

                return redirect('singleproject', id=project.id)
        else:
            project_form = NewProjectForm()
            image_form = Project_Image_Form()

        context = {
            'project_form': project_form,
            'image_form': image_form,
            'title': 'New Project'
        }

        return render(request, 'projects/newproject.html', context)

    else:
        return redirect("login")


@login_required
def deleteproject(request, id):
    project = get_object_or_404(Project, id=id)
    project_total_donation = Donate.get_total_donation_for_project(project)
    total_target = project.target_budget

    print("------------------- target", total_target.amount)
    print("------project_total_donation", project_total_donation)

    if project_total_donation < total_target.amount:
        project.delete()
        messages.warning(request, 'Project Deleted !!')

        return redirect('home')

    print("--------not valid -----------")
    messages.error(
        request, "You exceeded 25 '%' of your total target donation!")

    return redirect("singleproject", id=id)


@login_required
def editproject(request, id):
    project = get_object_or_404(Project, id=id)
    images = Image.objects.all().filter(project=project)
    print(images)
    # project=get_object_or_404(project,id=id,created_by=request.user)
    if request.method == 'POST':
        newproject = NewProjectForm(
            request.POST, request.FILES, instance=project)
        image_form = Project_Image_Form(
            request.POST, request.FILES, instance=project)
        if newproject.is_valid():
            print(request.POST)
            newproject.save()
            # Get the uploaded images and create an Image object for each one
        for image in request.FILES.keys():
            image_file = request.FILES.getlist(image)
            for i in image_file:
                fs = FileSystemStorage()
                filename = fs.save('images/projects/' + i.name, i)
                img = Image()
                img.image = filename
                img.project = project
                img.save()

            messages.success(
                request, "Project UPdated Successfully")

            return redirect('singleproject', id=project.id)
    elif request.method == 'GET':
        project_form = NewProjectForm(instance=project)
        images = Image.objects.all().filter(project=project)
        images.delete()
        context = {
            'project_form': project_form,
            'title': 'Edit Project'
        }
    return render(request, "projects/newproject.html", context)
