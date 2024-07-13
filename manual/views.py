import re
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from .models import Section, Subsection
from interactions.models import Favourite, Comment
from interactions.forms import CommentForm
from allauth.account.models import EmailAddress


# Create your views here.
def intro(request):
    return render(request, 'manual/intro.html')


def guide(request):
    return render(request, 'manual/guidelines.html')


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order.
    """
    return [int(text) if text.isdigit() else text for text in
            re.split(r'(\d+)', text)]


def section_list(request):
    sections = Section.objects.filter(~Q(title__in=['Introduction',
                                                    'Guidelines'])).order_by(
        'title')

    favourites = Favourite.objects.filter(
        user=request.user, section__in=sections).values_list(
        'section_id', flat=True) if request.user.is_authenticated else []

    # Convert queryset to list
    sections = list(sections)

    # Fetch first-level subsections and assign them to their respective
    # sections
    subsections = Subsection.objects.filter(
        parent__isnull=True).select_related('section').order_by('title')
    subsection_dict = {}
    for subsection in subsections:
        if subsection.section_id not in subsection_dict:
            subsection_dict[subsection.section_id] = []
        subsection_dict[subsection.section_id].append(subsection)

    for section in sections:
        section.subsections = subsection_dict.get(section.id, [])

    # Sort sections naturally
    sections.sort(key=lambda section: natural_keys(section.title))

    return render(request, 'manual/section_list.html',
                  {
                      'sections': sections,
                      'favourite_sections': favourites,
                  })


def section_detail_accordion(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = Subsection.objects.filter(section=section,
                                            parent__isnull=True).prefetch_related(
        Prefetch('sub_sections', queryset=Subsection.objects.order_by('title'))
    ).order_by('title')

    # Convert query sets to lists and sort naturally
    subsections = list(subsections)
    subsections.sort(key=lambda subsection: natural_keys(subsection.title))

    for subsection in subsections:
        subsection.subsections = sorted(list(subsection.sub_sections.all()),
                                        key=lambda subsubsection: natural_keys(
                                            subsubsection.title))

    comments = section.comments.filter(approved=True).order_by("-created_at")
    comment_count = comments.count()

    email_verified = EmailAddress.objects.filter(
        user=request.user,
        verified=True).exists() if request.user.is_authenticated else False

    form = CommentForm()

    # Get favourite sections and subsections for the logged-in user
    favourite_sections = Favourite.objects.filter(user=request.user,
                                                  section__isnull=False).values_list(
        'section_id', flat=True)
    favourite_subsections = Favourite.objects.filter(user=request.user,
                                                     subsection__isnull=False).values_list(
        'subsection_id', flat=True)

    return render(request, 'manual/section_detail_accordion.html', {
        'section': section,
        'subsections': subsections,
        'comments': comments,
        'form': form,
        'comment_count': comment_count,
        'email_verified': email_verified,
        'favourite_sections': favourite_sections,
        'favourite_subsections': favourite_subsections,
    })
