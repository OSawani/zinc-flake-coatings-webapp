from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Section, Subsection
from interactions.forms import CommentForm


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
    comments = subsection.comments.all().order_by("-created_at")
    comment_count = subsection.comments.filter(approved=True).count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.subsection = subsection
            comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your comment has been added')
            return redirect('subsection_detail', subsection_id=subsection.id)
    else:
        form = CommentForm()
    return render(request, 'manual/subsection_detail.html',
                  {
                      'subsection': subsection,
                      'comments': comments,
                      'form': form,
                  })
