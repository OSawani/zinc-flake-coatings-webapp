from django.shortcuts import render
from .models import Comment


# Create your views here.
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})
