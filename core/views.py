from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from manual.models import Section, Subsection
from django.contrib.auth import login
import jwt
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import User


def sso_login_view(request):
    """
    This view handles the SSO login process using a JWT token passed as a
    query parameter. It validates the token using the public key and logs
    in the user if a matching handbuch_user_id is found in the database.

    If the token is invalid, expired, or no matching user is found, the user
    is redirected to the homepage.
    """
    # Get the JWT token from the query parameter
    token = request.GET.get('jwt')
    if not token:
        return redirect('home')  # Redirect to the homepage if no token is present

    try:
        # Decode the JWT token using the public key
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT['VERIFYING_KEY'], algorithms=['RS256'])
        handbuch_user_id = decoded_token.get('sub')  # Extract the user ID from the token

        if not handbuch_user_id:
            return redirect('home')  # If the ID is not present, redirect to homepage

        # Find the user in the Django database based on handbuch_user_id
        try:
            user = User.objects.get(handbuch_user_id=handbuch_user_id)

            # Log the user in
            login(request, user)

            # Redirect to the homepage after successful login
            return redirect('home')
        except User.DoesNotExist:
            # If no matching user is found, redirect to the homepage
            return redirect('home')

    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        # If the token is invalid or expired, redirect to the homepage
        return redirect('home')


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
