from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Section, Subsection
from interactions.models import Favourite
from interactions.forms import CommentForm
from allauth.account.models import EmailAddress


# Create your views here.
def intro(request):
    return render(request, 'manual/intro.html')


def guide(request):
    return render(request, 'manual/guidelines.html')


def section_list(request):
    sections = Section.objects.filter(~Q(title__in=['Introduction',
                                                   'Guidelines'])).order_by(
        'title')
    favourites = Favourite.objects.filter(
        user=request.user, section__in=sections).values_list(
        'section_id', flat=True) if request.user.is_authenticated else []
    for section in sections:
        section.subsections = Subsection.objects.filter(
            section=section).order_by('title')
    return render(request, 'manual/section_list.html',
                  {
                      'sections': sections,
                      'favourite_sections': favourites,
                  }
                  )


def get_flat_subsections(section):
    subsections = Subsection.objects.filter(section=section).select_related('parent')
    subsection_dict = {None: []}
    for subsection in subsections:
        parent_id = subsection.parent_id if subsection.parent else None
        subsection_dict.setdefault(parent_id, []).append(subsection)
    return subsection_dict


def subsection_list(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsection_dict = get_flat_subsections(section)
    favourite_sections = Favourite.objects.filter(user=request.user,
                                                  section=section).values_list(
        'section_id', flat=True) if request.user.is_authenticated else []
    favourite_subsections = Favourite.objects.filter(
        user=request.user, subsection__in=Subsection.objects.filter(
            section=section)).values_list(
        'subsection_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'manual/subsection_list.html',
                  {
                      'section': section,
                      'subsection_dict': subsection_dict,
                      'favourite_sections': favourite_sections,
                      'favourite_subsections': favourite_subsections,
                  })


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

    # Determine if the subsection and section are favourites
    is_favourite_subsection = False
    is_favourite_section = False
    if request.user.is_authenticated:
        is_favourite_subsection = Favourite.objects.filter(
            user=request.user, subsection=subsection).exists()
        is_favourite_section = Favourite.objects.filter(
            user=request.user, section=subsection.section).exists()

    form = CommentForm()
    return render(request, 'manual/subsection_detail.html',
                  {
                      'subsection': subsection,
                      'comments': comments,
                      'form': form,
                      'comment_count': comment_count,
                      'email_verified': email_verified,
                      'is_favourite_subsection': is_favourite_subsection,
                      'is_favourite_section': is_favourite_section,
                  })


def section_detail(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = Subsection.objects.filter(
        section=section, parent__isnull=True).order_by(
        'title').prefetch_related('sub_sections')
    return render(request, 'manual/section_detail.html', {
        'section': section,
        'subsections': subsections,
    })
