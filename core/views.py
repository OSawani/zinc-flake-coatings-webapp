from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from manual.models import Section, Subsection


# Create your views here.
def home(request):
    """
    High-level description:
    This view renders the home page.

    **Context:**
    This view does not return any context variables.

    Template:
    This view returns the `core/home.html` template.
    """
    return render(request, 'core/home.html')


def search_results(request):
    """
    High-level description:
    This view handles the search functionality and displays search results
    for sections and subsections based on the user's query.

    model: `Section`, `Subsection`

    **Context:** - `sections`: A queryset of sections matching the search
    query, retrieved from the `Section` model. - `subsections`: A queryset
    of subsections matching the search query, retrieved from the
    `Subsection` model. - `query`: The search query string obtained from the
    GET parameters. - `page_obj`: The paginated search results.

    Template:
    This view returns the `core/search_results.html` template.
    """
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
