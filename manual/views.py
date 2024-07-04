import re
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from .models import Section, Subsection
from interactions.models import Favourite
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


def build_hierarchy(sections):
    """
    Build a hierarchy of sections and subsections.
    """
    # Create a dictionary of section IDs to section objects
    section_dict = {section.id: section for section in sections}

    for section in sections:
        section.subsections = []

    # Fetch all subsections for the given sections
    subsections = Subsection.objects.filter(section__in=sections).order_by(
        'title')

    for subsection in subsections:
        subsection.subsections = []
        if subsection.parent_id:
            # Check if parent_id is in section_dict before appending
            if subsection.parent_id in section_dict:
                section_dict[subsection.parent_id].subsections.append(
                    subsection)
            else:
                print(
                    f"Warning: Subsection {subsection.id} has parent {subsection.parent_id} which is not in section_dict")
        else:
            # Check if section_id is in section_dict before appending
            if subsection.section_id in section_dict:
                section_dict[subsection.section_id].subsections.append(
                    subsection)
            else:
                print(
                    f"Warning: Subsection {subsection.id} has section {subsection.section_id} which is not in section_dict")

    return list(section_dict.values())


def section_list(request):
    sections = Section.objects.filter(~Q(title__in=['Introduction',
                                                    'Guidelines'])).order_by(
        'title')

    favourites = Favourite.objects.filter(
        user=request.user, section__in=sections).values_list(
        'section_id', flat=True) if request.user.is_authenticated else []

    # Convert queryset to list
    sections = list(sections)

    # Build hierarchical structure
    sections = build_hierarchy(sections)

    # Sort sections naturally
    sections.sort(key=lambda section: natural_keys(section.title))

    return render(request, 'manual/section_list.html',
                  {
                      'sections': sections,
                      'favourite_sections': favourites,
                  })


def get_flat_subsections(section):
    subsections = Subsection.objects.filter(section=section).select_related(
        'parent')
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
            section=section)
    ).values_list(
        'subsection_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'manual/subsection_list_depr.html',
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

    email_verified = EmailAddress.objects.filter(
        user=request.user,
        verified=True).exists() if request.user.is_authenticated else False

    # Determine if the subsection and section are favourites
    is_favourite_subsection = Favourite.objects.filter(
        user=request.user,
        subsection=subsection).exists() if request.user.is_authenticated else False
    is_favourite_section = Favourite.objects.filter(
        user=request.user,
        section=subsection.section).exists() if request.user.is_authenticated else False

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
    css_path = section.css_path
    return render(request, 'manual/section_detail.html', {
        'section': section,
        'subsections': subsections,
        'css_path': css_path,
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

    return render(request, 'manual/section_detail_accordion.html', {
        'section': section,
        'subsections': subsections,
    })
