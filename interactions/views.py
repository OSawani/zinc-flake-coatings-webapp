from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm


# Create your views here.
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
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
        subsection_id = comment.subsection.id
        comment.delete()
        return redirect(
            'subsection_detail', subsection_id=comment.subsection.id)
    return render(request, 'interactions/delete_comment.html',
                  {'comment': comment})
