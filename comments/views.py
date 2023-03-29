from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.contrib import messages
# Create your views here.
from projects.models import Project
from comments.forms import CommentForm
from comments.models import Comments, Reply, ReportComment

from django.shortcuts import reverse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile

from django.contrib import messages


# @login_required


def addComment(request, id):
    project = Project.get_one_project(id)
    user = UserProfile.objects.get(username=request.user)

    if request.method == "POST":
        newCommentContent = CommentForm(request.POST)

        if newCommentContent.is_valid():
            # print("-------------------------------",
            #       newCommentContent.cleaned_data['comment_content'])

            newCommit = Comments(project=project,
                                 comment_content=newCommentContent.cleaned_data['comment_content'])
            newCommit.user = user
            newCommit.save()
            messages.info(request, "Comment added")

            return redirect("singleproject", id=id)
        else:
            commentForm = CommentForm()

        # return redirect(reverse("singleproject"), id=id,  kwargs={"id": id, 'form': form})
        return redirect("singleproject", id=id)


# @login_required
def addReply(request, project_id, comment_id):

   # project = get_object_or_404(Project, id=project_id)

    project = Project.get_one_project(project_id)

    user = UserProfile.objects.get(username=request.user)

    comment = Comments.objects.filter(id=comment_id).first()

    print("reply proj ---------", project)
    print("reply comment ---------", comment)

    if request.method == "POST":
        newReplyContent = CommentForm(request.POST)

        if newReplyContent.is_valid():
            # print("-------------------------------",
            #     newReplyContent.cleaned_data['comment_content'])
            # print("----------------user reply-------", request.user)

            newReply = Reply(comment_id=comment, project=project,
                             user=user,
                             reply_content=newReplyContent.cleaned_data['comment_content'])
            newReply.save()
            messages.info(request, 'Reply added !')

            return redirect("singleproject", id=project_id)
        else:
            commentForm = CommentForm()

        # return redirect(reverse("singleproject"), id=id,  kwargs={"id": id, 'form': form})
        return redirect("singleproject", id=project_id)


@login_required
def reportComment(request,  project_id, comment_id):
    comment = Comments.get_spesific_comment(comment_id)
    # print("----------replay comment ----------", comment)
    newReport = ReportComment(comment=comment, user=request.user)

    messages.warning(request, "you've reproted this comment")

    newReport.save()
    return redirect("singleproject", id=project_id)
