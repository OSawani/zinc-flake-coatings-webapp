from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from manual.models import Section, Subsection
from django.contrib.auth import login
from django.contrib import messages
import jwt
from .models import User
def sso_login_view(request):
    token = request.GET.get('jwt')
    if not token:
        return redirect(f"{reverse('home')}?error=1")

    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT['VERIFYING_KEY'], algorithms=['RS256'])
        handbook_user_id = decoded_token.get('handbook_user_id')

        if not handbook_user_id:
            return redirect(f"{reverse('home')}?error=1")

        # Find the user in the Django database and log in
        user = User.objects.get(handbuch_user_id=handbook_user_id)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        # Flash success message
        messages.success(request, f"Erfolgreich als {user.email} angemeldet.")
        return redirect('home')

    except User.DoesNotExist:
        return redirect(f"{reverse('home')}?error=1")
    except jwt.ExpiredSignatureError:
        return redirect(f"{reverse('home')}?error=1")
    except jwt.InvalidTokenError:
        return redirect(f"{reverse('home')}?error=1")

def home(request):
    """
    High-level description:
    This view renders the home page.

    **Context:**
    This view does not return any context variables.

    Template:
    This view returns the `core/home.html` template.
    """
    # Redirect to sso_login_view if 'jwt' is present and no error flag
    jwt_token = request.GET.get('jwt')
    if jwt_token and 'error' not in request.GET:
        # Redirect to sso_login_view, passing the jwt token as a query parameter
        return redirect(f"{reverse('sso_login')}?jwt={jwt_token}")

    # Otherwise, render the home page
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
