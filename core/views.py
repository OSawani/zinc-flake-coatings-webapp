from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from . import models
from manual.models import Section, Subsection


# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def search_results(request):
    query = request.GET.get('q')

    sections = Section.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    subsections = Subsection.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    all_results = list(sections) + list(subsections)

    paginator = Paginator(all_results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/search_results.html',
                  {
                      'sections': sections,
                      'subsections': subsections,
                      'query': query,
                      'page_obj': page_obj,
                  })
