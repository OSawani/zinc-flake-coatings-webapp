from django.shortcuts import render
from .models import Comment, Favourite, Notification


# Create your views here.
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})


def favorite_list(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'interactions/favourite_list.html',
                  {'favourites': favourites})


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'interactions/notification_list.html',
                  {'notifications': notifications})
