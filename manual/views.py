from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, Subsection
from interactions.forms import CommentForm
from allauth.account.models import EmailAddress


# Create your views here.
def section_list(request):
    sections = Section.objects.all()
    for section in sections:
        section.subsections = Subsection.objects.filter(section=section)
    return render(request, 'manual/section_list.html',
                  {'sections': sections})


def subsection_list(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = Subsection.objects.filter(section=section,
                                            parent__isnull=True)
    return render(request, 'manual/subsection_list.html',
                  {'section': section, 'subsections': subsections})


def subsection_detail(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)
    comments = subsection.comments.filter(approved=True).order_by(
        "-created_at")
    comment_count = comments.count()

    # Check if the user is authenticated and their email is verified
    email_verified = False
    if request.user.is_authenticated:
        email_verified = EmailAddress.objects.filter(user=request.user,
                                                     verified=True).exists()

    form = CommentForm()
    return render(request, 'manual/subsection_detail.html',
                  {
                      'subsection': subsection,
                      'comments': comments,
                      'form': form,
                      'comment_count': comment_count,
                      'email_verified': email_verified,
                  })
