from django.shortcuts import render, get_object_or_404
from .models import Section, Subsection


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
    comments = subsection.comments.all()
    return render(request, 'manual/subsection_detail.html',
                  {'subsection': subsection, 'comments': comments})
