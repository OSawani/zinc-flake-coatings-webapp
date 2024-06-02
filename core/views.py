from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Hello, world. You're at the core home page.")


def search(request):
    query = request.GET.get('q')
    # Search logic Implementation here
    results = []
    return render(request, 'core/search_results.html', {'results': results, 'query': query})