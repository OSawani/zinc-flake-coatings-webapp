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


def build_hierarchy(sections):
    """
    Build a hierarchy of sections and subsections.
    """
    return sections

def build_subsection_hierarchy(subsections):
    """
    Build a hierarchy of subsections.
    """
    # Create a dictionary to map subsections by their IDs
    subsection_dict = {subsection.id: subsection for subsection in subsections}

    # Initialize a list to hold the root subsections
    root_subsections = []

    # Iterate over each subsection
    for subsection in subsections:
        # Ensure the subsections attribute is set for each subsection
        setattr(subsection, 'subsections', [])
        # Check if the subsection has a parent
        if subsection.parent_id:
            # Get the parent subsection from the dictionary
            parent = subsection_dict[subsection.parent_id]
            # Append the current subsection to the parent's subsections list
            if not hasattr(parent, 'subsections'):
                setattr(parent, 'subsections', [])
            parent.subsections.append(subsection)
        else:
            # If no parent, it's a root subsection, so add it to the root list
            root_subsections.append(subsection)

    return root_subsections


def section_list(request):
    sections = Section.objects.filter(~Q(title__in=['Introduction',
                                                    'Guidelines'])).order_by(
        'title')

    favourites = Favourite.objects.filter(
        user=request.user, section__in=sections).values_list(
        'section_id', flat=True) if request.user.is_authenticated else []

    # Convert queryset to list
    sections = list(sections)

    # Fetch subsections and build hierarchy
    subsections = Subsection.objects.all().select_related('section', 'parent')
    subsection_dict = {}
    for subsection in subsections:
        if subsection.section_id not in subsection_dict:
            subsection_dict[subsection.section_id] = []
        subsection_dict[subsection.section_id].append(subsection)

    for section in sections:
        # Corrected attribute name to match the model's field
        section.subsections = build_subsection_hierarchy(
            subsection_dict.get(section.id, []))

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

    comments = section.comments.filter(approved=True).order_by("-created_at")
    comment_count = comments.count()

    email_verified = EmailAddress.objects.filter(
        user=request.user,
        verified=True).exists() if request.user.is_authenticated else False

    form = CommentForm()

    return render(request, 'manual/section_detail_accordion.html', {
        'section': section,
        'subsections': subsections,
        'comments': comments,
        'form': form,
        'comment_count': comment_count,
        'email_verified': email_verified,
    })
