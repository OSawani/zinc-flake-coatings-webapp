from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.models import EmailAddress
from .models import Comment
from .forms import CommentForm
from manual.models import Subsection


# Create your views here.
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})


def add_comment(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)
    email_verified = EmailAddress.objects.filter(user=request.user, verified=True).exists()

    if not email_verified:
        return render(request,
                      'interactions/email_not_verified.html')

    if not request.user.is_approved:
        return render(request, 'interactions/not_approved.html')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.subsection = subsection
            comment.approved = True  # Will change to False if
            # admin approval is needed in the future
            comment.save()
            return redirect('subsection_detail', subsection_id=subsection.id)
    else:
        form = CommentForm()

    return render(request, 'interactions/comment_form.html',
                  {'form': form, 'subsection': subsection})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = True # Will change to False if
            # admin approval is needed in the future
            form.save()
            messages.add_message(request, messages.SUCCESS,'Comment updated '
                                                           'successfully')
            return redirect(
                'subsection_detail', subsection_id=comment.subsection.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'interactions/edit_comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted '
                                                        'successfully')
        return redirect(
            'subsection_detail', subsection_id=comment.subsection.id)
    return render(request, 'interactions/delete_comment.html',
                  {'comment': comment})
